#!/usr/bin/env python
# -------------------------------------------------------------------------- #
# Copyright 2010-2011, Indiana University                                    #
#                                                                            #
# Licensed under the Apache License, Version 2.0 (the "License"); you may    #
# not use this file except in compliance with the License. You may obtain    #
# a copy of the License at                                                   #
#                                                                            #
# http://www.apache.org/licenses/LICENSE-2.0                                 #
#                                                                            #
# Unless required by applicable law or agreed to in writing, software        #
# distributed under the License is distributed on an "AS IS" BASIS,          #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.   #
# See the License for the specific language governing permissions and        #
# limitations under the License.                                             #
# -------------------------------------------------------------------------- #
"""
Command line front end for rain move
"""

__author__ = 'Javier Diaz'

import argparse
from getpass import getpass
import hashlib
import logging
import logging.handlers
import socket, ssl
import sys 
import time

from futuregrid_move.utils import fgLog
from futuregrid_move.rain.move.RainMoveClientConf import RainMoveClientConf

class RainMoveClient(object):
    def __init__(self, verbose):
        super(RainMoveClient, self).__init__()

        #Load Config
        self._conf = RainMoveClientConf()
        self.verbose = verbose
        
        self._port = self._conf.getPort()
        self._serveraddr = self._conf.getServeraddr()
        
        
        self._ca_certs = self._conf.getCaCerts()
        self._certfile = self._conf.getCertFile()
        self._keyfile = self._conf.getKeyFile()
        
        self._connMoveServer = None
        
        self.passwdtype = "ldappassmd5"
        #Setup log
        self._log = fgLog.fgLog(self._conf.getLogFile(), self._conf.getLogLevel(), "Rain Move Client", False)
        

    def connection(self):
        connected = False
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self._connMoveServer = ssl.wrap_socket(s,
                                        ca_certs=self._ca_certs,
                                        certfile=self._certfile,
                                        keyfile=self._keyfile,
                                        cert_reqs=ssl.CERT_REQUIRED,
                                        ssl_version=ssl.PROTOCOL_TLSv1)
            self._log.debug("Connecting server: " + self._serveraddr + ":" + str(self._port))
            self._connMoveServer.connect((self._serveraddr, self._port))   
            connected = True         
        except ssl.SSLError:
            self._log.error("CANNOT establish SSL connection. EXIT")
        except socket.error:
            self._log.error("Error with the socket connection")
        except:
            if self.verbose:
                print "Error CANNOT establish connection with the server"
            self._log.error("ERROR: exception not controlled" + str(sys.exc_info()))
        
        return connected
        #_connMoveServer.write(options) #to be done in each method
    def disconnect(self):
        try:
            self._connMoveServer.shutdown(socket.SHUT_RDWR)
            self._connMoveServer.close()
        except:
            self._log.debug("In disconnect:" + str(sys.exc_info()))

    def check_auth(self, userId, checkauthstat):
        endloop = False
        passed = False
        while not endloop:
            ret = self._connMoveServer.read(1024)
            if (ret == "OK"):
                if self.verbose:
                    print "Authentication OK. Your request is being processed"
                self._log.debug("Authentication OK")
                endloop = True
                passed = True
            elif (ret == "TryAuthAgain"):
                msg = "ERROR: Permission denied, please try again. User is " + userId                    
                self._log.error(msg)
                if self.verbose:
                    print msg                            
                m = hashlib.md5()
                m.update(getpass())
                passwd = m.hexdigest()
                self._connMoveServer.write(passwd)
            elif (ret == "NoActive"):                
                checkauthstat.append("ERROR: The status of the user " + userId + " is not active")
                checkauthstat.append("NoActive")
                self._log.error("The status of the user " + userId + " is not active")
                endloop = True
                passed = False
            elif (ret == "NoUser"):
                checkauthstat.append("ERROR: User " + userId + " does not exist")
                checkauthstat.append("NoUser")
                self._log.error("User " + userId + " does not exist")
                endloop = True
                passed = False
            else:                
                self._log.error(str(ret))
                #if self.verbose:
                #    print ret
                checkauthstat.append(str(ret))
                endloop = True
                passed = False
        return passed

    def cluster(self, user, passwd, subparser_name, operation, arguments, force):
        status=None
        start_all = time.time()
        checkauthstat = []
        msg = str(user) + "|" + str(passwd) + "|" + self.passwdtype + "|" + str(subparser_name) + "|" + str(operation) + "|" + str(arguments) + "|" + str(force)
        self._log.debug("Cluster: " + str(msg))
        self._connMoveServer.write(msg)
        
        if self.check_auth(user, checkauthstat):        
            
            status = self._connMoveServer.read(2048)
            
        else:
            self._log.error(str(checkauthstat[0]))
            if self.verbose:
                status = str(checkauthstat[0])
        
        end_all = time.time()
        self._log.info('TIME walltime rain move client (cluster):' + str(end_all - start_all))
        
        return status
        
    def node(self, user, passwd, subparser_name, operation, arguments, force):
        status=None
        start_all = time.time()
        checkauthstat = []

        msg = str(user) + "|" + str(passwd) + "|" + self.passwdtype + "|" + str(subparser_name) + "|" + str(operation) + "|" + str(arguments) + "|" + str(force)
        self._log.debug("Node: " + str(msg))
        self._connMoveServer.write(msg)
        
        if self.check_auth(user, checkauthstat):
            
            status = self._connMoveServer.read(2048)
            
        else:
            self._log.error(str(checkauthstat[0]))
            if self.verbose:
                status = str(checkauthstat[0])        
        
        end_all = time.time()
        self._log.info('TIME walltime rain move client (node):' + str(end_all - start_all))
        
        return status
        
    def service(self, user, passwd, subparser_name, operation, arguments, force):
        status = None
        start_all = time.time()
        checkauthstat = []
        
        msg = str(user) + "|" + str(passwd) + "|" + self.passwdtype + "|" + str(subparser_name) + "|" + str(operation) + "|" + str(arguments) + "|" + str(force)
        self._log.debug("Service: " + str(msg))
        self._connMoveServer.write(msg)
        
        if self.check_auth(user, checkauthstat):
            
            status = self._connMoveServer.read(2048)
            
        else:
            self._log.error(str(checkauthstat[0]))
            if self.verbose:
                status = str(checkauthstat[0])
        
        end_all = time.time()
        self._log.info('TIME walltime rain move client (service):' + str(end_all - start_all))
        
        return status
    
def main():

    verbose = True
    
    validTypes = ['hpc', 'eucalyptus', 'openstack', 'nimbus', 'opennebula']
    
    rainmoveclient = RainMoveClient(verbose)

    parser = argparse.ArgumentParser(prog="fg-move", formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="FutureGrid Image Registration Help ")    
    parser.add_argument('-u', '--user', dest='user', required=True, metavar='user', help='FutureGrid User name.')
    
    subparsers = parser.add_subparsers(dest='subparser_name', help='Positional arguments group different options that can be' 
                                       ' displayed by specifying <positional_argument> -h')
    
    subparser_cluster = subparsers.add_parser('cluster', help='Functionality to operate with clusters.')
    group_cluster = subparser_cluster.add_mutually_exclusive_group(required=True)
    group_cluster.add_argument('-c', '--create', metavar='clusterId', help='Create a new cluster.')
    group_cluster.add_argument('-r', '--remove', metavar='clusterId', help='Remove a cluster.')
    group_cluster.add_argument('-l', '--list', nargs='?', default="", metavar='clusterId', help='List available clusters or the information about a particular one.')
    group_cluster.add_argument('-f', '--force', default=False, action="store_true", help='Force operation.')
    
    subparser_node = subparsers.add_parser('node', help='Functionality to operate with nodes (machines)')
    group_node = subparser_node.add_mutually_exclusive_group(required=True)
    group_node.add_argument('-a', '--add', nargs=4, metavar=('nodeId', 'hostname', 'ip', 'cluster'), help='Add new node to a cluster.')
    group_node.add_argument('-r', '--remove', nargs=2, metavar=('nodeId', 'cluster'), help='Remove node. It is also removed from cluster and service.')
    group_node.add_argument('-i', '--info', metavar='nodeId', help='Information of a node.')
    group_node.add_argument('-f', '--force', default=False, action="store_true", help='Force operation.')
    
    
    subparser_service = subparsers.add_parser('service', help='Functionality to operate with services (infrastructures)')
    group_service = subparser_service.add_mutually_exclusive_group(required=True)
    group_service.add_argument('-c', '--create', nargs=2, metavar=('serviceId', 'type'), help='Create a new service.')
    group_service.add_argument('-a', '--add', nargs='+', metavar=('nodeId/s...','nodeId/s... serviceId'), help='Add node or list of nodes to a service. The last argument will be the service. I.e. -a node1 node2 service1 or -a node1 service1')
    group_service.add_argument('-r', '--remove', nargs='+', metavar=('nodeId/s...','nodeId/s... serviceId'), help='Remove node from a service.')
    group_service.add_argument('-m', '--move', nargs='+', metavar=('nodeId/s...','nodeId/s... serviceIdorigin serviceIddestination'), help='Move a node from one service to another.')
    group_service.add_argument('-l', '--list', nargs='?', default="", metavar='serviceId', help='List available services or the information about a particular one.')
    group_service.add_argument('-s', '--listfreenodes', nargs='?', default="", metavar='clusterId', help='List of nodes that are not assigned to any service.')
    subparser_service.add_argument('-f', '--force', default=False, action="store_true", help='The node will be removed/moved from the service and the instances/jobs running will be terminated.')
    

    args = parser.parse_args()

    
    
    print 'Starting Move Client...'
    
    #print args

    used_args = sys.argv[1:]

    #connect with the server
    print "Trying to connect with the server..."
    if not rainmoveclient.connection():
        print "ERROR: Connection with the server failed"
        sys.exit(1)

    
    print "Please insert the password for the user " + args.user + ""
    m = hashlib.md5()
    m.update(getpass())
    passwd = m.hexdigest()
    
    if (args.subparser_name == 'cluster'):
        
        if args.create != None:
            
            print rainmoveclient.cluster(args.user, passwd, args.subparser_name, "create", args.create, args.force)
        elif args.remove != None:
            print rainmoveclient.cluster(args.user, passwd, args.subparser_name, "remove", args.remove, args.force)
        elif ('-l' in used_args or '--list' in used_args):
            print rainmoveclient.cluster(args.user, passwd, args.subparser_name, "lists", args.list, args.force)
        else:
            print "ERROR: you must to specify one of the cluster's options. \n"
            subparser_cluster.print_help()
        
    elif (args.subparser_name == 'node'):
        
        if args.add != None:
            print rainmoveclient.node(args.user, passwd, args.subparser_name, "add", args.add, args.force)
        elif args.remove != None:
            print rainmoveclient.node(args.user, passwd, args.subparser_name, "remove", args.remove, args.force)
        elif args.info != None:
            print rainmoveclient.node(args.user, passwd, args.subparser_name, "info", args.info, args.force)
        else:
            print "ERROR: you must to specify one of the node's options. \n"
            subparser_node.print_help()
            
    elif (args.subparser_name == 'service'):

        if args.create != None:
            if args.create[1].lower() in validTypes:
                print rainmoveclient.service(args.user, passwd, args.subparser_name, "create", args.create, args.force)
            else:
                print "ERROR: Type of service not recognized. Valid types are: " + str(validTypes)
        elif args.add != None:
            if len(args.add) < 2:
                print "ERROR: you need to specify at least two arguments: nodeId and serviceId"
            else:
                print rainmoveclient.service(args.user, passwd, args.subparser_name, "add", args.add, args.force)            
        elif args.remove != None:
            if len(args.remove) < 2:
                print "ERROR: you need to specify at least two arguments: nodeId and serviceId"
            else:
                print rainmoveclient.service(args.user, passwd, args.subparser_name, "remove", args.remove, args.force)
        elif args.move != None:
            if len(args.move) < 3:
                print "ERROR: you need to specify at least three arguments: nodeId serviceIdorigin serviceIddestination"
            else:
                print rainmoveclient.service(args.user, passwd, args.subparser_name, "move", args.move, args.force)
        elif ('-l' in used_args or '--list' in used_args):
            print rainmoveclient.service(args.user, passwd, args.subparser_name, "lists", args.list, args.force)
        elif ('-s' in used_args or '--listfreenodes' in used_args):
            print rainmoveclient.service(args.user, passwd, args.subparser_name, "listfreenodes", args.list, args.force)
        else:
            print "ERROR: you must to specify one of the service's options. \n"
            subparser_service.print_help()
            
if __name__ == "__main__":
    main()
#END

