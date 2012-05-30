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
Description: Server to do the real operations in the machines. Install software in machine and add/remove from infrastructure.
"""
__author__ = 'Javier Diaz'

from types import *
import re
import logging
import logging.handlers
import random
from random import randrange
import os
import sys
import socket, ssl
from multiprocessing import Process
from subprocess import *
import time

from futuregrid_move.rain.move.RainMoveServerConf import RainMoveServerConf

class RainMoveServerSites(object):

    def __init__(self):
        super(RainMoveServerSites, self).__init__()
        
               
        self.numparams = 3
        

        #load from config file
        self._rainSitesConf = RainMoveServerConf()
        self._rainSitesConf.load_moveSiteServerConfig() 
        
        self.port = self._rainSitesConf.getMoveSitePort()
        self.proc_max = self._rainSitesConf.getMoveSiteProcMax()
        self.refresh_status = self._rainSitesConf.getMoveSiteRefreshStatus()
        self.log_filename = self._rainSitesConf.getMoveSiteLog()
        self.logLevel = self._rainSitesConf.getMoveSiteLogLevel()
        
        self._ca_certs = self._rainSitesConf.getMoveSiteServerCaCerts()
        self._certfile = self._rainSitesConf.getMoveSiteServerCertFile()
        self._keyfile = self._rainSitesConf.getMoveSiteServerKeyFile()
        
        
        print "\nReading Configuration file from " + self._rainSitesConf.getConfigFile() + "\n"
        
        self.logger = self.setup_logger("")
        
        
    def setup_logger(self, extra):
        #Setup logging        
        logger = logging.getLogger("RainMoveServerSites" + extra)
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
        
        proc_list = []
        total_count = 0
        while True:        
            if len(proc_list) == self.proc_max:
                full = True
                while full:
                    for i in range(len(proc_list) - 1, -1, -1):
                        #self.logger.debug(str(proc_list[i]))
                        if not proc_list[i].is_alive():
                            #print "dead"                        
                            proc_list.pop(i)
                            full = False
                    if full:
                        time.sleep(self.refresh_status)
            
            total_count += 1
            #channel, details = sock.accept()
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
                #print connstream                                
                proc_list.append(Process(target=self.process_client, args=(connstream, fromaddr[0])))            
                proc_list[len(proc_list) - 1].start()
            except ssl.SSLError:
                self.logger.error("Unsuccessful connection attempt from: " + repr(fromaddr))
                self.logger.info("Rain Move Site Server Request DONE")
            except socket.error:
                self.logger.error("Error with the socket connection")
                self.logger.info("Rain Move Site Server Request DONE")
            except:
                self.logger.error("Uncontrolled Error: " + str(sys.exc_info()))
                if type(connstream) is ssl.SSLSocket: 
                    connstream.shutdown(socket.SHUT_RDWR)
                    connstream.close() 
                self.logger.info("Rain Move Site Server Request DONE")
    
                
    def process_client(self, connstream, fromaddr):
        start_all = time.time()
        self.logger = self.setup_logger("." + str(os.getpid()))
        self.logger.info('Accepted new connection')
        
        #receive the message
        data = connstream.read(2048)
        self.logger.debug("msg received: " + data)
        params = data.split(',')
        #print data
        #params[0] is service (infrastructure) name.
        #params[1] is the operation
        #params[2] is the operation argument
        
        
        service = params[0].strip()
        operation = params[1].strip()
        argument = params[2].strip()
        #MORE PARAMETERS ARE NEEDED
        #operation site, infrastructure origin, infrastructure destination, number machines,
        #reinstall?, image source, partitions,
                
        if len(params) != self.numparams:
            msg = "ERROR: incorrect message"
            self.errormsg(connstream, msg)
            return

        #DO STUFFS
        #Think if we should created classes for each infrastructure and use polymorphism OR it is easy enough to just use methods.  
        
        if operation == 'add':
            self.logger.debug("Add machine " + argument + " to the service " + service)
            
        elif operation == 'remove':
            self.logger.debug("Remove machine " + argument + " from the service " + service)            
        else:
            self.logger.debug("Operation " + operation + " Service " + service + " Argument " + argument)           
        
        connstream.write("True")
        try:
            connstream.shutdown(socket.SHUT_RDWR)
            connstream.close()
        except:
            self.logger.error("ERROR: " + str(sys.exc_info()))

    def errormsg(self, connstream, msg):
        self.logger.error(msg)
        try:
            connstream.write(msg)
            connstream.shutdown(socket.SHUT_RDWR)
            connstream.close()
        except:
            self.logger.debug("In errormsg: " + str(sys.exc_info()))
        self.logger.info("Rain Move Site Server DONE")
        
def main():

    #Check if we have root privs 
    #if os.getuid() != 0:
    #    print "Sorry, you need to run with root privileges"
    #    sys.exit(1)

    print "\n The user that executes this must have sudo with NOPASSWD"

    server = RainMoveServerSites()
    server.start()

if __name__ == "__main__":
    main()
#END        