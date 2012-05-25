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


def main():

    parser = argparse.ArgumentParser(prog="fg-register", formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="FutureGrid Image Registration Help ")    
    
    parser.add_argument('-u', '--user', dest='user', required=True, metavar='user', help='FutureGrid User name')
    
    subparsers = parser.add_subparsers(help='sub-command help')
    
    subparser_cluster = subparsers.add_parser('cluster', help='cluster help')
    subparser_cluster.add_argument('--create', metavar='clusterId', help='Create a new cluster.')
    subparser_cluster.add_argument('--remove', metavar='clusterId', help='Remove a cluster.')
    subparser_cluster.add_argument('--list', nargs = '?', metavar='clusterId', help='List available clusters or the information about a particular one.')
    
    subparser_node = subparsers.add_parser('node', help='node help')
    subparser_node.add_argument('--add', nargs=4, metavar=('nodeId','hostname','ip','cluster'), help='Add new node to a cluster.')
    subparser_node.add_argument('--remove', nargs=2, metavar=('nodeId','cluster'), help='Remove node from cluster.')
    subparser_node.add_argument('--info', metavar='nodeId', help='Information of a node.')
    
    subparser_service = subparsers.add_parser('service', help='service help')
    subparser_service.add_argument('--create', metavar='serviceId', help='Create a new service.')
    subparser_service.add_argument('--add', nargs=2, metavar=('nodeId','serviceId'), help='Add node to a service.')
    subparser_service.add_argument('--remove', nargs=2, metavar=('nodeId','serviceId'), help='Remove node from a service.')
    subparser_service.add_argument('--move', nargs=3, metavar=('nodeId','serviceIdorigin','serviceIddestination'), help='Move a node from one service to another.')
    subparser_service.add_argument('--list', nargs = '?', metavar='serviceId', help='List available services or the information about a particular one.')

    args = parser.parse_args()
    
    print 'Starting Move Client...'
    
    print args

    print args.add
    
if __name__ == "__main__":
    main()
#END

