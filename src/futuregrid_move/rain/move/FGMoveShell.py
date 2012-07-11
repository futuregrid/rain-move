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
import logging
import logging.handlers

from Resource import Resource, Node, Cluster, Service
from HPCService import HPCService
from EucaService import EucaService
from OpenStackService import OpenStackService
from NimbusService import NimbusService
from Fabric import Fabric, Inventory, InventoryFile, InventoryDB
from RainMoveServerConf import RainMoveServerConf

class FGMoveShell(Cmd):
    '''fg-move: Cloud shifting shell command'''

    pp = pprint.PrettyPrinter(indent=0)
    
    # logger
    logger = logging.getLogger("FGMoveShell")
    logger.setLevel(logging.DEBUG)    
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler = logging.FileHandler("fgmoveshell.log")
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    
        
    # load configuration
    _moveConf = RainMoveServerConf()
    _moveConf.load_moveServerConfig()
    
    fgfabric = Fabric(_moveConf, logger, True)
    
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
        print "You are leaving the FutureGrid Fabric Management/rain-move shell"
    
    @options([
        make_option('-f', '--file', type="string",
                    help="load from filename"),
        make_option('-d', '--db', type="string",
                    help="load from database")
        ])
    def do_bootstrap(self, args, opts):
        '''bootstrap the whole fabric from an inventory.
        objects for nodes, clusters, and services would be created.
        '''
        if opts.file:
            filename = opts.file
            #print filename
            fginventory = InventoryFile(filename)
            self.fgfabric.load(fginventory)
    
    def do_set(self, args, silent=False):
        '''set default context - node, cluster, or service
        If no name/identifier provided, following operations would be applied for that class/objects.
        Otherwise operations would be applied on the specific object - e.g., a cluster called india.
        '''
        args = ''.join(args)
        args = re.split(" ", args)
        cat = args[0]
        method = "get" + cat.lower().title()
        if len(args) > 1:
            obj = args[1]
        else:
            obj = None
        self._currentObj = getattr(self.fgfabric, method)(obj)

        # context - class, general
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
        # context - a node object
        elif isinstance(self._currentObj, Node):
            self._currentCls = "Node"
            print self._currentObj.identifier
        # context - a cluster object
        elif isinstance(self._currentObj, Cluster):
            self._currentCls = "Cluster"
            if not silent:
                print "Default Cluster is set to: " + self._currentObj.identifier
            #print self._currentObj.list()
        # context - a service object
        elif isinstance(self._currentObj, Service):
            self._currentCls = "Service"
            if not silent:
                print "Default Service is set to: " + self._currentObj.identifier
                print "\t Type: " + self._currentObj.type
            #print self._currentObj.list()
        else:
            print "Wrong parameter provided!"
    
    def supportGroupOps(self, curCls):
        # what class has implemented the group operations methods, like list()?
        if curCls in ("Cluster", "Service"):
            return True
        else:
            return False   
                 
    def do_listall(self, args):
        ''' list all based on the context'''
        # list identifier only
        if isinstance(self._currentObj, dict):
            for key in sorted(self._currentObj.keys()):
                print key
        # list nodes
        elif self.supportGroupOps(self._currentCls):
            for anodeid in sorted(self._currentObj.list().keys()):
                print anodeid
            
    def do_nodeinfo(self, args):
        '''print out node info specified by the node identifier'''
        if args in self.fgfabric.getNode().keys():
            print self.fgfabric.getNode()[args]
    
    @options([
        make_option('-c', '--cluster', type="string",
                    help="cluster name"),
        make_option('-s', '--service', type="string",
                    help="service name")
        ])
    def do_add(self, args, opts):
        '''add new node; existing node to a cluster; existing node to a service, etc.
        '''
        args = ''.join(args)
        args = re.split(" ", args)
        # add a new node
        if self._currentCls == 'Node':
            #construcing a node from args
            #accepting format of: id,name,ip,cluster
            newnode = Node(args[0], args[1], args[2], args[3])
            allnodes = self.fgfabric.getNode().values()
            allnodes.append(newnode)
            self.fgfabric.updateNodes(allnodes)
            self.do_set('Node', True) # fix cache
        # move a node into a cluster. The node must be added/created first if not exist.
        elif self._currentCls == 'Cluster':
            existingnode = self.fgfabric.getNode(args[0])
            # current context is class/general
            # need -c option to specify which cluster to operate on
            if isinstance(self._currentObj, dict):
                clustername = opts.cluster
                if clustername:
                    # retrieve the cluster
                    cluster = self.fgfabric.getCluster(clustername)                    
                    if existingnode:
                        cluster.add(existingnode)
                        self.fgfabric.store()
                        self.do_set('Cluster', True) # fix cache
                    else:
                        print "node does not exist in the node list.\nPlease add node first!"
                else:
                    print "cluster name is required"
            # current context already set to specific cluster
            else:
                if existingnode:
                    self._currentObj.add(existingnode)
                    self.fgfabric.store()
                    self.do_set('Cluster ' + self._currentObj.identifier, True) # fix cache
                else:
                    print "node does not exist in the node list.\nPlease add node first!"            
        # move a node into a service. This internally invokes the implementations for specific service types.    
        elif self._currentCls == 'Service':
            existingnode = self.fgfabric.getNode(args[0])
            # context class/general, requires -s option
            if isinstance(self._currentObj, dict):
                servicename = opts.service
                if servicename:
                    service = self.fgfabric.getService(servicename)                    
                    print existingnode
                    if existingnode:
                        service.add(existingnode)
                        self.fgfabric.store()
                        self.do_set('Service', True) # fix cache
                    else:
                        print "node does not exist in the node list.\nPlease add node first!"
                else:
                    print "service name is required"
            # context was already set to a specific service
            else:
                self._currentObj.add(existingnode)
                self.fgfabric.store()
                self.do_set('Service ' + self._currentObj.identifier, True) # fix cache
        # context not supported
        else:
            print "Type Error!"
    
    def do_remove(self, args):
        '''remove a node - opposite of the add'''
        # operation on the class in general
        # only operate on node, but not a cluster/service
        if isinstance(self._currentObj, dict):
            print "Removing a whole cluster/service is not supported from this tool"
        # operation on an object - a real cluster or service
        # dispatch the call to the implementation for the class
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
