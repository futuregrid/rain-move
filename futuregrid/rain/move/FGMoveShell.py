#!/usr/bin/env python
'''FG Move (Fabric Management) shell'''

#import argparse
#import os
import re
import pprint
import optparse
from cmd2 import Cmd
from cmd2 import make_option
from cmd2 import options
import unittest
import sys

from Resource import Resource, Node, Cluster, Service
from HPCService import HPCService
from EucaService import EucaService
from OpenStackService import OpenStackService
from NimbusService import NimbusService
from Fabric import Fabric, Inventory, InventoryFile, InventoryDB

class FGMoveShell(Cmd):
    '''fg-move: Cloud shifting shell command'''

    pp = pprint.PrettyPrinter(indent=0)
    fgfabric = Fabric()
    _currentObj = None
    _currentCls = None
    echo = True
    timing = True
    #debug = True

    prompt = "fg-move> "

    logo = """
  _____       _                   ____      _     _
 |  ___|_   _| |_ _   _ _ __ ___ / ___|_ __(_) __| |
 | |_  | | | | __| | | | '__/ _ \ |  _| '__| |/ _` |
 |  _| | |_| | |_| |_| | | |  __/ |_| | |  | | (_| |
 |_|    \__,_|\__|\__,_|_|  \___|\____|_|  |_|\__,_|
----------------------------------------------------
    """
    
    def preloop(self):
        print self.logo

    def postloop(self):
        print "BYE FORM GREGOR"
    
    @options([
        make_option('-f', '--file', type="string",
                    help="load from filename"),
        make_option('-d', '--db', type="string",
                    help="load from database")
        ])
    def do_bootstrap(self, args, opts):        
        if opts.file:
            filename = opts.file
            #print filename
            fginventory = InventoryFile(filename)
            self.fgfabric.load(fginventory)
    
    def do_set(self, args, silent=False):
        args = ''.join(args)
        args = re.split(" ", args)
        cat = args[0]
        method = "get" + cat.lower().title()
        if len(args) > 1:
            obj = args[1]
        else:
            obj = None
        self._currentObj = getattr(self.fgfabric, method)(obj)
        
        if isinstance(self._currentObj, dict):
            aobj = self._currentObj.values()[0]
            if isinstance(aobj, Node):
                self._currentCls = "Node"
            elif isinstance(aobj, Cluster):
                self._currentCls = "Cluster"
            elif isinstance(aobj, Service):
                self._currentCls = "Service"
            else:
                self._currentCls = "Not Defined"
            if not silent:
                print "Set default operation on Class: " + self._currentCls
            #for key in self._currentObj:
            #    print key
        elif isinstance(self._currentObj, Node):
            self._currentCls = "Node"
            print self._currentObj.identifier
        elif isinstance(self._currentObj, Cluster):
            self._currentCls = "Cluster"
            if not silent:
                print "Default Cluster is set to: " + self._currentObj.identifier
            #print self._currentObj.list()
        elif isinstance(self._currentObj, Service):
            self._currentCls = "Service"
            if not silent:
                print "Default Service is set to: " + self._currentObj.identifier
                print "\t Type: " + self._currentObj.type
            #print self._currentObj.list()
        else:
            print "Wrong parameter provided!"
    
    def supportGroupOps(self, curCls):
        if curCls in ("Cluster", "Service"):
            return True
        else:
            return False   
                 
    def do_listall(self, args):
        # list identifier only
        if isinstance(self._currentObj, dict):
            for key in self._currentObj.keys():
                print key
        # list nodes
        elif self.supportGroupOps(self._currentCls):
            for anodeid in self._currentObj.list().keys():
                print anodeid
            
    def do_nodeinfo(self, args):
        if args in self.fgfabric.getNode().keys():
            print self.fgfabric.getNode()[args]
    
    @options([
        make_option('-c', '--cluster', type="string",
                    help="cluster name"),
        make_option('-s', '--service', type="string",
                    help="service name")
        ])
    def do_add(self, args, opts):
        args = ''.join(args)
        args = re.split(" ", args)    
        if self._currentCls == 'Node':
            #construcing a node from args
            #accepting format of: id,name,ip,cluster
            newnode = Node(args[0], args[1], args[2], args[3])
            allnodes = self.fgfabric.getNode().values()
            allnodes.append(newnode)
            self.fgfabric.updateNodes(allnodes)
            self.do_set('Node', True) # fix cache
        elif self._currentCls == 'Cluster':
            existingnode = self.fgfabric.getNode(args[0])
            if isinstance(self._currentObj, dict):
                clustername = opts.cluster
                if clustername:
                    cluster = self.fgfabric.getCluster(clustername)                    
                    if existingnode:
                        cluster.add(existingnode)
                        self.do_set('Cluster', True) # fix cache
                    else:
                        print "node does not exist in the node list.\nPlease add node first!"
                else:
                    print "cluster name is required"
            else:
                if existingnode:
                    self._currentObj.add(existingnode)
                    self.do_set('Cluster ' + self._currentObj.identifier, True) # fix cache
                else:
                    print "node does not exist in the node list.\nPlease add node first!"            
            
        elif self._currentCls == 'Service':
            existingnode = self.fgfabric.getNode(args[0])
            if isinstance(self._currentObj, dict):
                service = opts.service
                if servicename:
                    service = self.fgfabric.getService(servicename)                    
                    print existingnode
                    if existingnode:
                        service.add(existingnode)
                        self.do_set('Service', True) # fix cache
                    else:
                        print "node does not exist in the node list.\nPlease add node first!"
                else:
                    print "service name is required"
            else:
                self._currentObj.add(existingnode)
                self.do_set('Service ' + self._currentObj.identifier, True) # fix cache
        else:
            print "Type Error!"
    
    def do_remove(self, args):
        # operation on the class in general
        if isinstance(self._currentObj, dict):
            print "Removing a whole cluster/service is not supported"
        # operation on an object - a real cluster or service
        elif self.supportGroupOps(self._currentCls):
            self._currentObj.remove(args)
               
    def do_testfg(self, args):
        print self.fgfabric.info()

def main():
    parser = optparse.OptionParser()
    parser.add_option('-t', '--test',
                      dest='unittests',
                      action='store_true',
                      default=False,
                      help='Run unit test suite')
    (callopts, callargs) = parser.parse_args()
    if callopts.unittests:
        sys.argv = [sys.argv[0]]  # the --test argument upsets unittest.main()
        unittest.main()
    else:
        app = FGMoveShell()
        app.cmdloop()

if __name__ == '__main__':
    main()
