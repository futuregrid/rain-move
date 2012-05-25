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


__author__ = 'Javier Diaz'

import logging
import logging.handlers
import os
import re
import socket
import ssl
import sys
import time

from Resource import Resource, Node, Cluster, Service
from HPCService import HPCService
from EucaService import EucaService
from OpenStackService import OpenStackService
from NimbusService import NimbusService
from Fabric import Fabric, Inventory, InventoryFile, InventoryDB

from RainMoveServerConf import RainMoveServerConf

class RainMoveServer(object):

    def __init__(self, inventoryFile):
        super(RainMoveServer, self).__init__()
        
        self.numparams = 5   #prefix,name,os,arch,machine
        
        self.fgfabric = Fabric()  #Fabric object
        
        if inventoryfile != None:
            self.load(inventoryfile)
        
        #load from config file
        self._rainConf = RainMoveServerConf()
        self._rainConf.load_moveServerConfig() 
        
        self.port = self._rainConf.getMovePort()
        self.log_filename = self._rainConf.getMoveLog()
        self.logLevel = self._rainConf.getMoveLogLevel()
        
        self._ca_certs = self._rainConf.getMoveServerCaCerts()
        self._certfile = self._rainConf.getMoveServerCertFile()
        self._keyfile = self._rainConf.getMoveSiteServerKeyFile()
        
        self._clientca_certs = self._rainConf.getMoveClientCaCerts()
        self._clientcertfile = self._rainConf.getMoveClientCertFile()
        self._clientkeyfile = self._rainConf.getMoveClientKeyFile()
        
        
        print "\nReading Configuration file from " + self._rainSitesConf.getConfigFile() + "\n"
        
        self.logger = self.setup_logger("")
                
    def load(self, inventoryfile):
        fginventory = InventoryFile(inventoryfile)
        self.fgfabric.load(fginventory)
    
    def setup_logger(self):
        #Setup logging
        logger = logging.getLogger("RainMoveServer")
        logger.setLevel(self.logLevel)    
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler = logging.FileHandler(self.log_filename)
        handler.setLevel(self.logLevel)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False #Do not propagate to others
        
        return logger
    
    def start(self):  
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', self.port))
        sock.listen(1)
        self.logger.info('Starting Server on port ' + str(self.port))
        while True:
            newsocket, fromaddr = sock.accept()
            connstream = 0
            try:
                connstream = ssl.wrap_socket(newsocket,
                              server_side=True,
                              ca_certs=self._ca_certs,
                              cert_reqs=ssl.CERT_REQUIRED,
                              certfile=self._certfile,
                              keyfile=self._keyfile,
                              ssl_version=ssl.PROTOCOL_TLSv1)
                self.process_client(connstream)
            except ssl.SSLError:
                self.logger.error("Unsuccessful connection attempt from: " + repr(fromaddr))
            finally:
                if connstream is ssl.SSLSocket:
                    connstream.shutdown(socket.SHUT_RDWR)
                    connstream.close()
                

    def process_client(self, connstream):
        self.logger.info('Accepted new connection')
        #receive the message
        data = connstream.read(2048)
        params = data.split(',')

        #params[0] is element (cluster or service)
        #params[1] is elementname (india, sierra, indiahpc, sierraeuca..)
        #params[2] is operation (add, remove, list, info)
        #params[3] is machine            
        #params[4] is arguments

        self.element = params[0]
        self.elementname = params[1]
        self.operation = params[2]
        self.machine = params[3]
        self.arguments = params[4]
        

        if len(params) != self.numparams:
            msg = "ERROR: incorrect message"
            self.errormsg(connstream, msg)
            return

            #TODOOOOO

            if status != 0:
                msg = 'ERROR: including image name in image.txt file'
                self.logger.debug(msg)
                self.errormsg(connstream, msg)
                return
            else:
                connstream.write('OK')
                connstream.shutdown(socket.SHUT_RDWR)
                connstream.close()

        
            self.logger.info("Rain Move Server DONE")
        
    def add(self):
        pass
    
    def remove(self):
        pass
    
    def info(self):
        pass
    
    def list(self):
        pass   

    def errormsg(self, connstream, msg):
        self.logger.error(msg)
        try:
            connstream.write(msg)
            connstream.shutdown(socket.SHUT_RDWR)
            connstream.close()
        except:
            self.logger.debug("In errormsg: " + str(sys.exc_info()))
        self.logger.info("Rain Move Server DONE")

   

def main():
    
    parser = argparse.ArgumentParser(prog="fg-register", formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="FutureGrid Image Registration Help ")    
    parser.add_argument('-l', '--load', dest='inventoryFile', metavar='inventoryFile', required=True, 
                        help='File that contains the machines/services inventory')
    
        
    args = parser.parse_args()
    
    server = RainMoveServer(args.inventoryFile)
    server.start()

if __name__ == "__main__":
    main()
#END
