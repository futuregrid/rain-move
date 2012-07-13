"""
This module contains the definitions of classes for
Resource, Node, Cluster, and Service

"""

__author__ = 'Fugang Wang'
__version__ = '0.1'

import abc
import json
import socket, ssl
import logging
import logging.handlers
import sys

from futuregrid_move.rain.move.RainMoveServerConf import RainMoveServerConf

from teefaa.teefaa import Teefaa

class Resource(object):
    '''Abstract base class for Resource'''
    __metaclass__ = abc.ABCMeta

    # possible types
    TYPE = dict(zip(("NODE", "VM", "IP"),
                    ("Node", "VM", "IP"))
               )
    
    @abc.abstractproperty
    def type(self):
        '''
        abstract property - type of the resource
        '''
        return "abstrct property"

    @abc.abstractproperty
    def identifier(self):
        '''
        abstract property - identifier of the resource
        It must be unique among all nodes from all clusters we have
        '''
        return "abstract property"

    @abc.abstractmethod
    def info(self):
        '''
        abstract method - string info that represents the resource
        '''
        return "abstract method"
        
class Node(Resource):
    '''Node implementation of the Resource abstract class'''

    def __init__(self, id, name="", ip="", cluster=""):
        '''
        constructor of node object

        param id: node identifier
        '''
        self._id = id
        self._name = name
        self._ip = ip
        self._cluster = cluster
        self._type = Resource.TYPE["NODE"] # Resource type is set to 'Node'
        self._allocated = "FREE" # Resource is initially free - not assigned to any service.
        
    @property
    def type(self):
        return self._type

    @property
    def identifier(self):
        return self._id

    @property
    def allocated(self):
        '''
        Check if the node is allocated
        
        return: 'FREE' for a free node; or the service identifier that the node being allocated to
        '''
        return self._allocated

    @allocated.setter
    def allocated(self, svcName):
        '''
        Allocate a node to a service, or set to 'FREE'

        param svcName: service identifier, or 'FREE'
        '''
        self._allocated = svcName

    @property
    def ip(self):
        '''
        Get Node's public IP address
        '''
        return self._ip
        
    @ip.setter
    def ip(self, newip):
        '''
        Set/assign a public IP address to the node

        param ip: string in format of 'xxx.xxx.xxx.xxx' which is a valid and available IP address
        '''
        self._ip = newip
        
    @property
    def name(self):
        '''
        Internal name when calling within the cluster.
        E.g., i55
        '''
        return self._name
        
    @name.setter
    def name(self, newname):
        '''
        Set the internal name
        '''
        self._name = newname
    
    @property
    def cluster(self):
        '''
        cluster name where the node belongs to
        E.g., hotel
        '''
        return self._cluster
        
    @cluster.setter
    def cluster(self, newname):
        '''
        Set the cluster name
        '''
        self._cluster = newname
            
    def info(self):
        '''
        Implemented the abstract method to display the node info as a string

        return: a string in json format represents the node
        '''
        return str(json.dumps(dict([('Type', self.type), ('Identifier', self.identifier), ('Name', self.name), ('IP', self.ip), ('Cluster', self.cluster), ('isAllocated', self.allocated)])))
        
    def __repr__(self):
        '''
        string representation of the object
        '''
        return self.info()

class Cluster(object):
    '''
    Cluster class which is a set of nodes
    '''
    def __init__(self, id, hosts=()):
        '''
        constructor

        param hosts: a list of Node object
        '''
        self._id = id
        self._hosts = dict()
        for host in hosts:
            # stored in dict format - node identifier as key and the node object constructed as value
            self._hosts[host.identifier] = host

    @property
    def identifier(self):
        return self._id
        
    def add(self, ahost):
        '''
        add a new node into the cluster

        param ahost: a node object
        type ahost: Node
        '''
        if not isinstance(ahost, Node):
            ret = False
        else:
            ahost.cluster = self.identifier
            self._hosts[ahost.identifier] = ahost
            ret = True
        return ret
    
    def remove(self, ahost):
        '''
        remove a node from the cluster

        param ahost: a node object
        type ahost: Node
        '''
        self._hosts[ahost.identifier].cluster("")
        del self._hosts[ahost.identifier]
    
    def get(self, ahostid):
        '''
        get a host by its identifier

        param ahostid: host identifier
        return ahost: the host with the specified identifier
        type ahost: Node type
        '''
        ret = None
        if ahostid in self._hosts:
            ret = self._hosts[ahostid]
        return ret
                
    def list(self):
        '''
        list all nodes belong to the cluster
        '''
        return self._hosts

class Service(object):
    '''
    Service abstract class
    A service is a set of allocated resources organized in such a way that resources could be easily managed.
    The resources could be node, public IP address, etc.
    '''
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self._MoveClientca_certs=None
        self._MoveClientcertfile=None
        self._MoveClientkeyfile=None
        self._address=None
        self._port=None
        self.logger = None
        self.verbose = True
        self.teefaaobj = None
    
    def setTeefaa(self, teefaaobj):
        self.teefaaobj=teefaaobj
        
    def setLogger(self, log):
        self.logger=log
        
    def setVerbose(self, verbose):
        self.verbose=verbose
        
    def load_config(self, moveConf):
        self._MoveClientca_certs = moveConf.getMoveClientCaCerts()
        self._MoveClientcertfile = moveConf.getMoveClientCertFile()
        self._MoveClientkeyfile = moveConf.getMoveClientKeyFile()
        
        if moveConf.loadMoveRemoteSiteConfig(self._type, self._id):
            self._address=moveConf.getMoveRemoteSiteAddress()
            self._port= moveConf.getMoveRemoteSitePort()
            success = True
        else:
            success = False
        return success
    """
    @abc.abstractmethod
    def doadd(self, ares):
        '''
        abstract method to be implemented in concrete service implementation classes
        It deals with the actual processing that add a node into the service

        param ares: a resource to be added
        type ares: Resource type, e.g., Node
        '''
        ###################################
        # Implementation to add into a service
        ###################################
        print "abstract method. Will be implemented in concrete classes"
        return True
    """    
    @abc.abstractmethod
    def cbadd(self, ares):
        '''
        callback to deal with any data persistence as well as clean up
        e.g., write the new allocation info into db
        '''
        ###################################
        # TODO: node, service data Persistence; any clean up...
        ###################################
        print "abstract method. Will be implemented in concrete classes"
        return True
    """
    @abc.abstractmethod
    def doremove(self, ares):
        '''
        abstract method to be implemented in concrete service implementation classes
        It deals with the actual processing that remove a node from the service

        param ares: a resource to be removed
        type ares: Resource type, e.g., Node
        '''
        ###################################
        # Need to check if the node is free, i.e., no job is running, no reseration, etc.
        ###################################
        print "abstract method. Will be implemented in concrete classes"
        return True
    """   
    @abc.abstractmethod
    def cbremove(self, ares):
        '''
        callback to deal with any data persistence as well as clean up
        e.g., write the new allocation info into db
        '''
        ###################################
        # TODO: node, service data Persistence; any clean up...
        ###################################
        print "abstract method. Will be implemented in concrete classes"
        return True

    ######################
    # common properties
    ######################
    
    @property
    def identifier(self):
        return self._id

    @property
    def type(self):
        return self._type


    ######################
    # common methods
    ######################
    
    def socketConnection(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            connection = ssl.wrap_socket(s,
                                        ca_certs=self._MoveClientca_certs,
                                        certfile=self._MoveClientcertfile,
                                        keyfile=self._MoveClientkeyfile,
                                        cert_reqs=ssl.CERT_REQUIRED,
                                        ssl_version=ssl.PROTOCOL_TLSv1)
            
            msg="Connecting server: " + self._address + ":" + str(self._port)
            if self.verbose:
                print msg    
            self.logger.debug(msg)
            
            connection.connect((self._address, self._port))
            
        except ssl.SSLError:
            msg = "ERROR: CANNOT establish SSL connection. EXIT"
            if self.verbose:
                print msg
            self.logger.debug(msg)            
            connection = None
        except socket.error:
            msg = "ERROR: CANNOT establish connection with RainMoveServerSites service. EXIT"
            if self.verbose:
                print msg
            self.logger.debug(msg)
            connection = None
        return connection
    
    def socketCloseConnection(self, connstream):
        try:
            connstream.shutdown(socket.SHUT_RDWR)
            connstream.close()
        except:
            self.logger.error("ERROR: closing connection. " + str(sys.exc_info()))
    
    def list(self):
        return self._res
        
    def get(self, aresid):
        '''
        get a resource by its identifier

        param aresid: resource identifier
        return ares: the resource with the specified identifier
        type ares: Resource type
        '''
        ret = None
        if aresid in self._res:
            ret = self._res[aresid]
        return ret
        
    def add(self, ares):
        '''
        add a resource to the service.
        This should be the one to call from outside. It deals with precondition check,
        e.g. asserting the resource to be added is 'Free'. It will call the actual doadd()
        implementation method for processing and cbadd() method for clean up

        param ares: a resource to be added
        type ares: Resource type, e.g., Node
        '''
        ret = False
        msg = ""
        if isinstance(ares, Resource):
            # has to be a free node
            if(ares.allocated == 'FREE'):
##AKIIIIIIIIIIIII
                success, retstatus = self.doadd(ares)
                #success = True
                #retstatus =""
                if success:
                    self._res[ares.identifier] = ares
                    ares.allocated = self.identifier
                    #self.cbadd(ares)
                    ret = True
                else:
                    msg = "ERROR: add operation failed. " + str(retstatus)
                    if self.verbose:
                        print msg
                    self.logger.error(msg)
                        
            else:
                msg = "ERROR: " + ares.identifier + " is not free - allocated to: " + ares.allocated
                if self.verbose:
                    print msg
                self.logger.error(msg)
                
        return ret, msg

    def remove(self, aresid, force):
        '''
        remove a resource from the service.
        This should be the one to call from outside. It deals with precondition check,
        e.g. asserting the resource to be added is 'Free'. It will call the actual doremove()
        implementation method for processing and cbremove() for clean up

        param aresid: a resource to be removed
        type aresid: identifier string of the resource to be removed
        '''
        ret = False
        msg = ""
        ares = self.get(aresid)
        # has to be being allocated in THE service
        if ares is not None:
#AKIIIII
            success, retstatus = self.doremove(ares, force)
            #success = True
            #retstatus =""
            if success:
                del self._res[ares.identifier]
                ares.allocated = 'FREE'
                #self.cbremove(ares)
                ret = True
            else:
                msg = "ERROR: remove operation failed. " + str(retstatus)
                if self.verbose:
                    print msg
                self.logger.error(msg)
                
        else:
            msg = "ERROR: " + aresid + " does not belong to the service " + self.identifier
            if self.verbose:
                print msg
            self.logger.error(msg)
            
        return ret, msg

    def doadd(self, ares): #This is the same in all the sub classes
        success = False
        
        msg = "INSIDE " + self._type + "Service:doadd: add into " + self._type + " service"
        self.logger.debug(msg)
        if self.verbose:
            print msg
        
        msg = "Calling Teefaa provisioning"
        self.logger.debug(msg)
        if self.verbose:
            print msg
            
        status = self.teefaaobj.provision(ares.name, self._type, ares.cluster)        
        
        if status != 'OK':
            self.logger.error(status)
            if self.verbose:
                print status
            success = False
            msg = status
        else:
            msg = "Teefaa provisioned the host " + ares.name + " of the site " + ares.cluster + " with the os " + self._type + " successfully"
            self.logger.debug(msg)
            if self.verbose:
                print msg
                    
            msg = "Calling RainMoveSite to ensure the node is active in the service"
            self.logger.debug(msg)
            if self.verbose:
                print msg
            
            connection=self.socketConnection()
            if connection != None:
                connection.write(self._type + ", add, " + ares.name)
                status = connection.read(1024)
                msg = status
                self.socketCloseConnection(connection)
                if status == "OK":
                    success = True
                else:
                    success = False
                    self.logger.error(status)
                    if self.verbose:
                        print status                
            else:
                msg = "ERROR: Connecting with the remote site. The node was not allocated to the service."
                self.logger.error(msg)
                if self.verbose:
                    print msg        
        
        return success, msg

    def doremove(self, ares, force): #This is the same in all the classes. We should move it to the father
        success = False
        
        msg = "INSIDE " + self._type + "Service:doremove: remove from " + self._type + " service"
        self.logger.debug(msg)
        if self.verbose:
            print msg
        
        connection=self.socketConnection()
        if connection != None:
            connection.write(self._type + ",remove," + ares.name + ","+ str(force))
            status = connection.read(1024)
            self.socketCloseConnection(connection)
            msg=status
            if status == "OK":
                success = True
            else:
                success = False
                self.logger.error(status)
                if self.verbose:
                    print status       
        else:
            msg = "ERROR: Connecting with the remote site. The node was not removed."
            self.logger.error(msg)
            if self.verbose:
                print msg
        
        return success, msg
