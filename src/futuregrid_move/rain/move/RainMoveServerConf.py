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
Class to read Rain Move Server configuration
"""

__author__ = 'Javier Diaz'

import os
import ConfigParser
import string
import sys
import logging
import re


configFileName = "fg-server.conf"

class RainMoveServerConf(object):

    ############################################################
    # init
    ############################################################

    def __init__(self):
        super(RainMoveServerConf, self).__init__()

        self._fgpath = ""
        try:
            self._fgpath = os.environ['FG_PATH']
        except KeyError:
            self._fgpath = os.path.dirname(__file__) + "/../../"

        ##DEFAULT VALUES##
        self._localpath = "~/.fg/"

        self._configfile = os.path.expanduser(self._localpath) + "/" + configFileName
        #print self._configfile
        if not os.path.isfile(self._configfile):
            self._configfile = "/etc/futuregrid/" + configFileName #os.path.expanduser(self._fgpath) + "/etc/" + configFileName
            #print self._configfile
            #if not os.path.isfile(self._configfile):
            #    self._configfile = os.path.expanduser(os.path.dirname(__file__)) + "/" + configFileName
                #print self._configfile
            if not os.path.isfile(self._configfile):   
                print "ERROR: configuration file "+configFileName+" not found"
                sys.exit(1)
        
        #move server
        
        self._Moveport = 0
        self._MoveauthorizedUsers = []
        self._Movelog = ""
        self._MovelogLevel = ""   
        self._MoveServerca_certs = ""
        self._MoveServercertfile = ""
        self._MoveServerkeyfile = ""
        self._Moveproc_max = 0
        self._Moverefresh_status = 0
        
        self._MoveClientca_certs = ""
        self._MoveClientcertfile = ""
        self._MoveClientkeyfile = ""
        
        self._MoveRemoteSiteAddress=""
        self._MoveRemoteSitePort=0

        #move site server
        self._MoveSiteport = 0
        self._MoveSiteproc_max = 0
        self._MoveSiterefresh_status = 0
        #self._MoveSitenopasswdusers = {}  #dic {'user':['ip','ip1'],..}
        self._MoveSitelog = ""
        self._MoveSitelogLevel = ""
        self._MoveSitemax_wait = 0 
        self._MoveSiteEc2varfile = ""
        self._MoveSiteServerca_certs = ""
        self._MoveSiteServercertfile = ""
        self._MoveSiteServerkeyfile = ""
        
        
        self._logLevel_default = "DEBUG"
        self._logType = ["DEBUG", "INFO", "WARNING", "ERROR"]
        
        self._config = ConfigParser.ConfigParser()
        self._config.read(self._configfile)

    ############################################################
    # getConfigFile
    ############################################################
    def getConfigFile(self):
        return self._configfile
    
    #move server

    def getMovePort(self):
        return self._Moveport

    def getMoveProcMax(self):
        return self._Moveproc_max
    def getMoveRefreshStatus(self):
        return self._Moverefresh_status

    def getMoveAuthorizedUsers(self):
        return self._MoveauthorizedUsers
    def getMoveLog(self):
        return self._Movelog
    def getMoveLogLevel(self):
        return self._MovelogLevel
    def getMoveServerCaCerts(self):
        return self._MoveServerca_certs
    def getMoveServerCertFile(self): 
        return self._MoveServercertfile
    def getMoveServerKeyFile(self): 
        return self._MoveServerkeyfile

    def getMoveClientCaCerts(self):
        return self._MoveClientca_certs
    def getMoveClientCertFile(self): 
        return self._MoveClientcertfile
    def getMoveClientKeyFile(self): 
        return self._MoveClientkeyfile
    
    def getMoveRemoteSiteAddress(self):
        return self._MoveRemoteSiteAddress
    def getMoveRemoteSitePort(self):
        return self._MoveRemoteSitePort
    
    #move site server
    def getMoveSitePort(self):
        return self._MoveSiteport
    
    def getMoveSiteProcMax(self):
        return self._MoveSiteproc_max
    def getMoveSiteRefreshStatus(self):
        return self._MoveSiterefresh_status
    """
    def getMoveSiteNoPasswdUsers(self):
        return self._MoveSitenopasswdusers
    """
    def getMoveSiteLog(self):
        return self._MoveSitelog
    def getMoveSiteLogLevel(self):
        return self._MoveSitelogLevel
    def getMovesiteMaxWait(self):
        return self._MoveSitemax_wait
    def getMoveSiteEc2varfile(self):
        return self._MoveSiteEc2varfile
    def getMoveSiteServerCaCerts(self):
        return self._MoveSiteServerca_certs
    def getMoveSiteServerCertFile(self): 
        return self._MoveSiteServercertfile
    def getMoveSiteServerKeyFile(self): 
        return self._MoveSiteServerkeyfile

    
    ############################################################
    # load_moveServerConfig
    ############################################################
    def load_moveServerConfig(self):        
        section = "RainMoveServer"

        try:
            self._Moveport = int(self._config.get(section, 'port', 0))
        except ConfigParser.NoOptionError:
            print "Error: No port option found in section " + section + " file " + self._configfile
            sys.exit(1)
        except ConfigParser.NoSectionError:
            print "Error: no section "+section+" found in the "+self._configfile+" config file"
            sys.exit(1)
        try:
            self._Moveproc_max = int(self._config.get(section, 'proc_max', 0))
        except ConfigParser.NoOptionError:
            print "Error: No proc_max option found in section " + section + " file " + self._configfile
            sys.exit(1)
        try:
            self._Moverefresh_status = int(self._config.get(section, 'refresh', 0))
        except ConfigParser.NoOptionError:
            print "Error: No refresh option found in section " + section + " file " + self._configfile
            sys.exit(1)
        try:
            aux = self._config.get(section, 'authorizedusers', 0)
            aux1 = aux.split(",")
            for i in aux1:
                if (i.strip() != ""):
                    self._MoveauthorizedUsers.append(i.strip())
        except ConfigParser.NoOptionError:
            print "No authorizedusers option found in section " + section + " file " + self._configfile
            sys.exit(1)
        try:
            self._Movelog = os.path.expanduser(self._config.get(section, 'log', 0))
        except ConfigParser.NoOptionError:
            print "Error: No log option found in section " + section + " file " + self._configfile
            sys.exit(1)
        try:
            tempLevel = string.upper(self._config.get(section, 'log_level', 0))
        except ConfigParser.NoOptionError:
            tempLevel = self._logLevel_default
        if not (tempLevel in self._logType):
            print "Log level " + tempLevel + " not supported. Using the default one " + self._logLevel_default
            tempLevel = self._logLevel_default
        self._MovelogLevel = eval("logging." + tempLevel)
        try:
            self._MoveServerca_certs = os.path.expanduser(self._config.get(section, 'ca_cert', 0))
        except ConfigParser.NoOptionError:
            print "Error: No ca_cert option found in section " + section + " file " + self._configfile
            sys.exit(1)
        if not os.path.isfile(self._MoveServerca_certs):
            print "Error: ca_cert file not found in "  + self._MoveServerca_certs 
            sys.exit(1)
        try:
            self._MoveServercertfile = os.path.expanduser(self._config.get(section, 'certfile', 0))
        except ConfigParser.NoOptionError:
            print "Error: No certfile option found in section " + section + " file " + self._configfile
            sys.exit(1)
        if not os.path.isfile(self._MoveServercertfile):
            print "Error: certfile file not found in "  + self._MoveServercertfile 
            sys.exit(1)
        try:
            self._MoveServerkeyfile = os.path.expanduser(self._config.get(section, 'keyfile', 0))
        except ConfigParser.NoOptionError:
            print "Error: No keyfile option found in section " + section + " file " + self._configfile
            sys.exit(1)
        if not os.path.isfile(self._MoveServerkeyfile):
            print "Error: keyfile file not found in "  + self._MoveServerkeyfile
            sys.exit(1)

        try:
            self._MoveClientca_certs = os.path.expanduser(self._config.get(section, 'Clientca_cert', 0))
        except ConfigParser.NoOptionError:
            print "Error: No Clientca_cert option found in section " + section + " file " + self._configfile
            sys.exit(1)
        if not os.path.isfile(self._MoveClientca_certs):
            print "Error: Clientca_cert file not found in "  + self._Moveca_certs 
            sys.exit(1)
        try:
            self._MoveClientcertfile = os.path.expanduser(self._config.get(section, 'Clientcertfile', 0))
        except ConfigParser.NoOptionError:
            print "Error: No Clientcertfile option found in section " + section + " file " + self._configfile
            sys.exit(1)
        if not os.path.isfile(self._MoveClientcertfile):
            print "Error: Clientcertfile file not found in "  + self._MoveClientcertfile 
            sys.exit(1)
        try:
            self._MoveClientkeyfile = os.path.expanduser(self._config.get(section, 'Clientkeyfile', 0))
        except ConfigParser.NoOptionError:
            print "Error: No Clientkeyfile option found in section " + section + " file " + self._configfile
            sys.exit(1)
        if not os.path.isfile(self._MoveClientkeyfile):
            print "Error: Clientkeyfile file not found in "  + self._MoveClientkeyfile 
            sys.exit(1)
        
    def loadMoveRemoteSiteConfig(self, service, site):
        '''
        service is eucalyptus, openstack, ...
        site is india, sierra...
        '''
        status = True
        self._config.read(self._configfile)
        section = "Move-" + service.lower() + "-" +site.lower()
                
        try:
            self._MoveRemoteSiteAddress = self._config.get(section, 'address', 0)
        except ConfigParser.NoOptionError:
            self._MoveRemoteSiteAddress = ""
            status = False
        except ConfigParser.NoSectionError:
            status = False
            return status
            #return "ERROR: No section Move-" + service.lower() + "-" +site.lower() + " in file " + self._configfile
        try:
            self._MoveRemoteSitePort = int(self._config.get(section, 'port', 0))
        except ConfigParser.NoOptionError:
            self._MoveRemoteSitePort = 0
            status = False
        except ConfigParser.NoSectionError:
            status = False
        
        return status

    ############################################################
    # load_moveServerConfig
    ############################################################
    def load_moveSiteServerConfig(self):        
        section = "RainMoveSiteServer"
        try:
            self._MoveSiteport = int(self._config.get(section, 'port', 0))
        except ConfigParser.NoOptionError:
            print "Error: No port option found in section " + section + " file " + self._configfile
            sys.exit(1)
        except ConfigParser.NoSectionError:
            print "Error: no section "+section+" found in the "+self._configfile+" config file"
            sys.exit(1)
       
        try:
            self._MoveSiteproc_max = int(self._config.get(section, 'proc_max', 0))
        except ConfigParser.NoOptionError:
            print "Error: No proc_max option found in section " + section + " file " + self._configfile
            sys.exit(1)
        try:
            self._MoveSiterefresh_status = int(self._config.get(section, 'refresh', 0))
        except ConfigParser.NoOptionError:
            print "Error: No refresh option found in section " + section + " file " + self._configfile
            sys.exit(1)
        """
        try:
            aux = self._config.get(section, 'nopasswdusers', 0).strip()
            aux = "".join(aux.split()) #REMOVE ALL WHITESPACES
            parts = aux.split(";")
            for i in parts:         
                temp = i.split(":")
                if len(temp) == 2:                    
                    self._MoveSitenopasswdusers[temp[0]] = temp[1].split(",")            
        except ConfigParser.NoOptionError:            
            pass
        """
        try:
            self._MoveSitelog = os.path.expanduser(self._config.get(section, 'log', 0))
        except ConfigParser.NoOptionError:
            print "Error: No log option found in section " + section + " file " + self._configfile
            sys.exit(1)
        try:
            tempLevel = string.upper(self._config.get(section, 'log_level', 0))
        except ConfigParser.NoOptionError:
            tempLevel = self._logLevel_default
        if not (tempLevel in self._logType):
            print "Log level " + tempLevel + " not supported. Using the default one " + self._logLevel_default
            tempLevel = self._logLevel_default
        self._MoveSitelogLevel = eval("logging." + tempLevel)
        
        try:
            self._MoveSitemax_wait = int(self._config.get(section, 'max_wait', 0))
        except ConfigParser.NoOptionError:
            print "Error: No max_wait option found in section " + section + " file " + self._configfile
            sys.exit(1)
        try:
            self._MoveSiteEc2varfile = os.path.expanduser(self._config.get(section, 'ec2varfile', 0))
        except ConfigParser.NoOptionError:
            print "Warning: No ec2varfile option found in section " + section + " file " + self._configfile
        if not os.path.isfile(self._MoveSiteEc2varfile):
            print "Warning: ec2varfile file not found in "  + self._MoveSiteEc2varfile      
        try:
            self._MoveSiteServerca_certs = os.path.expanduser(self._config.get(section, 'ca_cert', 0))
        except ConfigParser.NoOptionError:
            print "Error: No ca_cert option found in section " + section + " file " + self._configfile
            sys.exit(1)
        if not os.path.isfile(self._MoveSiteServerca_certs):
            print "Error: ca_cert file not found in "  + self._MoveSiteServerca_certs 
            sys.exit(1)
        try:
            self._MoveSiteServercertfile = os.path.expanduser(self._config.get(section, 'certfile', 0))
        except ConfigParser.NoOptionError:
            print "Error: No certfile option found in section " + section + " file " + self._configfile
            sys.exit(1)
        if not os.path.isfile(self._MoveSiteServercertfile):
            print "Error: certfile file not found in "  + self._MoveSiteServercertfile 
            sys.exit(1)
        try:
            self._MoveSiteServerkeyfile = os.path.expanduser(self._config.get(section, 'keyfile', 0))
        except ConfigParser.NoOptionError:
            print "Error: No keyfile option found in section " + section + " file " + self._configfile
            sys.exit(1)
        if not os.path.isfile(self._MoveSiteServerkeyfile):
            print "Error: keyfile file not found in "  + self._MoveSiteServerkeyfile
            sys.exit(1)
