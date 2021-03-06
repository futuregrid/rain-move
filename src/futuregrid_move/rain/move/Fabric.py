"""
The Fabric module

"""

__author__ = 'Fugang Wang, Javier Diaz'
__version__ = '0.1'


import pymongo
from pymongo import Connection
from bson import ObjectId
  
import abc
import json
import re
import logging
import logging.handlers
import sys

from futuregrid_move.rain.move.Resource import Resource, Node, Cluster, Service
from futuregrid_move.rain.move.EucaService import EucaService
from futuregrid_move.rain.move.OpenStackService import OpenStackService
from futuregrid_move.rain.move.NimbusService import NimbusService
from futuregrid_move.rain.move.HPCService import HPCService

#from teefaa.teefaa import Teefaa
from teefaa.api import baremetal_provisioning

class Inventory(object):
    '''Abstract base class that defines inventory for a fabric.
    read(), and write() methods have to be implemented'''
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def read(self):
        '''
        load the inventory info and returns a dict object in the format of:
        {'nodes':[[node1id, node1name, node1ip], ...],
        'clusters':{clusteridentifier:[[node1id, node1name, node1ip], ...], ...},
        'services':{serviceidentifier:{'nodes':[node1id, node2id, ...], 'type':servicetype}, ...}
        }
        '''
        return
    
    @abc.abstractmethod
    def write(self, data):
        '''
        write the updated dict object as defined in the read() per data persistence method.
        '''
        return

class InventoryMongoDB(Inventory):
    def __init__(self, DBaddress, DBport, DBname):
        success = False
        self._res = dict()        
        self._dbConnection=None
        self._mongoAddress = DBaddress
        self._mongoDBName = DBname
        self._mongoPort = DBport
    
    ############################################################
    # mongoConnection
    ############################################################
    def mongoConnection(self):
        """connect with the mongos available
        
        return: Connection object if succeed or False in other case
        
        """
        #TODO: change to a global connection??                
        connected = False
        try:
            self._dbConnection = Connection(self._mongoAddress, self._mongoPort)
            connected = True

        except pymongo.errors.ConnectionFailure as detail:
            print "ERROR: Connection failed for " + self._mongoAddress
        except TypeError:
            print "ERROR: TypeError in InventoryMongoDB - mongoConnection"

        return connected

    def read(self):
        nodes = []
        clusters = dict()
        services = dict()
        
        dbLink = self._dbConnection[self._mongoDBName]
        
        for i in dbLink.collection_names():
            
            if re.search("^cluster",i):
                clustername = i.split("_")[1].lower().encode('ascii','ignore')
                clusters[clustername] = []
                for j in dbLink[i].find():
                    nodes.append([j['id'].encode('ascii','ignore'),j['name'].encode('ascii','ignore'),
                                  j['ip'].encode('ascii','ignore'),j['cluster'].encode('ascii','ignore')])
                    clusters[clustername].append([j['id'].encode('ascii','ignore'),j['name'].encode('ascii','ignore'),
                                                  j['ip'].encode('ascii','ignore'),j['cluster'].encode('ascii','ignore')])                        
            elif re.search("^service",i):
                servicetype = i.split("_")[1].lower().encode('ascii','ignore')
                servicename = i.split("_")[2].lower().encode('ascii','ignore')
                services[servicename] = dict()
                services[servicename]['type'] = servicetype
                services[servicename]['nodes'] = []
                for j in dbLink[i].find():
                    services[servicename]['nodes'].append(j['nodeid'].encode('ascii','ignore'))

        ret = {"nodes":nodes, "clusters":clusters, "services":services}
        return ret     
      
    def createCluster(self, clusterName):
        dbLink = self._dbConnection[self._mongoDBName]
        dbLink.create_collection("cluster_"+clusterName)
        
    def addNode2Cluster(self, node):
        '''node is a Node object, cluster is the id'''
        dbLink = self._dbConnection[self._mongoDBName]
        collection = dbLink["cluster_"+node.cluster]
        
        meta = {"id": node.identifier,
                "name": node.name,
                "ip" : node.ip,
                "cluster" : node.cluster,
                }
                
        collection.insert(meta, safe=True)

    def createService(self, serviceName, type):
        dbLink = self._dbConnection[self._mongoDBName]
        dbLink.create_collection("service_"+type.lower()+"_"+serviceName)
   
    def addNode2Service(self, nodeId, serviceName, serviceType):
        dbLink = self._dbConnection[self._mongoDBName]
        collection = dbLink["service_"+serviceType.lower()+"_"+serviceName]
        meta = {"nodeid": nodeId }                
        collection.insert(meta, safe=True)
    
    def removeNodeFromService(self, nodeId, serviceName, serviceType):
        dbLink = self._dbConnection[self._mongoDBName]
        collection = dbLink["service_"+serviceType.lower()+"_"+serviceName]
        
        collection.remove({"nodeid": nodeId}, safe=True)
    
    def fromMemory2DB(self, nodes, services):
        """res: resource dictionary that contains nodes, clusters and services"""

        #drop database        
        self._dbConnection.drop_database(self._mongoDBName)
        
        for i in nodes:
            self.addNode2Cluster(i)

        for i in services:
            self.createService(i.identifier, i.type)
            for j in i.list().keys():
                self.addNode2Service(j, i.identifier, i.type)
    
    def write(self, data):
        #it should not be needed as we update the db in every operation
        print "Store function Not needed"

class InventoryFile(Inventory):
    '''
    Deprecated:
    file based implementation for the inventory class'''
    def __init__(self, fname):
        self._cfgfile = fname
        self._res = dict()
        return
    
    def getResources(self):
        return self._res
    
    def read(self):
        '''reading from file'''
        file_inv = open(self._cfgfile)
        content = file_inv.read()
        file_inv.close()
        nodes = []
        clusters = dict()
        services = dict()
        current = None
        #print lines
        lines = re.split("\n", content)
        for line in lines:
            if line:
                #print line
                linesregex = re.compile('\[(.+)\]')
                m = linesregex.match(line)
                #section header
                if m is not None:
                    header = m.group(1)
                    headerclusterregex = re.compile('CLUSTER:(.+)')
                    m = headerclusterregex.match(header)
                    if m is not None:
                        clustername = m.group(1).lower()
                        #print clustername
                        clusters[clustername] = []
                        current = clusters[clustername]
                    #not in format of 'CLUSTER:xxx'
                    else:
                        headerserviceregex = re.compile('SERVICE:(.+):(.+)')
                        m = headerserviceregex.match(header)
                        servicetype = m.group(1).lower()
                        servicename = m.group(2).lower()
                        services[servicename] = dict()
                        services[servicename]['type'] = servicetype
                        services[servicename]['nodes'] = []
                        current = services[servicename]['nodes']
                        #print servicetype, servicename
                #node list
                else:
                    nodeallregex = re.compile('(.+),(.*),(.*)')
                    m = nodeallregex.match(line)
                    #node list for cluster in form of: identifier,name,ip
                    if m is not None:
                        resId = m.group(1)
                        name = m.group(2)
                        ip = m.group(3)
                        #print resId, name, ip
                        nodes.append([resId,name,ip,clustername])
                        current.append([resId,name,ip,clustername])
                        
                    #node list for service in format of: identifier
                    else:
                        nodeidregex = re.compile('(.+)')
                        m = nodeidregex.match(line)
                        if m is not None:
                            resId = m.group(1)
                            current.append(resId)
                        else:
                            print "ERROR"
                    #print line
        ret = {"nodes":nodes, "clusters":clusters, "services":services}
        #print ret
        return ret
    
    def write(self, data):
        '''construct strings from he updated data and write it to file'''
        clusters = data['clusters']
        services = data['services']
        file_inv = open(self._cfgfile, 'w')
        str2print = ''
        # write cluster data first
        for acluster in sorted(clusters.keys()):
            clustername = acluster
            cluster = clusters[clustername]
            # section header for each cluster
            str2print += '[CLUSTER:' + clustername.upper() + ']\n'
            clusternodes = cluster.list()
            for anodeid in sorted(clusternodes.keys()):
                node = clusternodes[anodeid]
                str2print += node.identifier + ',' + node.name + ',' + node.ip + '\n'
            str2print += '\n'

        # write servcie data
        for aservice in sorted(services.keys()):
            servicename = aservice
            service = services[servicename]
            servicetype = service.type
            # header for each service
            str2print += '[SERVICE:' + servicetype.upper() + ":" + servicename.upper() + ']\n'
            servicenodes = service.list()
            for anodeid in sorted(servicenodes.keys()):
                node = servicenodes[anodeid]
                str2print += node.identifier + '\n'
            str2print += '\n'
        file_inv.write(str2print)
        file_inv.close()
        return

class InventoryDB(Inventory):
    '''database based implementation class for inventory'''
    def __init__(self, config):
        return
    
    def read(self):
        return
    
    def write(self):
        return
                    
class Fabric(object):
    '''Fabric class that defines a set of nodes, clusters, and services'''
    # service type and classname mapping
    svctype = {'hpc':'HPC', 'eucalyptus':'Euca', 'nimbus':'Nimbus', 'openstack':'OpenStack'}
    def __init__(self, moveConf, logger, verbose=True, nodes=(), clusters=(), services=()):
        self._moveConf=moveConf
        self.logger=logger
        self.verbose=verbose
        self._inventory = None
        self._nodes={}
        self._clusters={}
        self._services={}
        
        #self.teefaaobj=Teefaa() #default config file (fg-server.conf) and no verbose
        
        self.update(nodes, clusters, services)
    
    def loadGetNodesServices(self, inventory):
        '''load data from inventory to bootstrap the fabric'''
        #print inventory.__class__.__name__
        self._inventory = inventory
        data = self._inventory.read()
        if self.verbose:
            print data
        else:
            self.logger.debug(str(data))
        _nodes = []
        _clusters = []
        _services = []
        nodesdata = data['nodes']
        clustersdata = data['clusters']
        servicesdata = data['services']
        for node in nodesdata:
            _nodes.append(Node(node[0],node[1],node[2],node[3]))
        self.updateNodes(_nodes)
        for clustername in clustersdata.keys():
            acluster = Cluster(clustername)
            clusterdata = clustersdata[clustername]
            for nodedata in clusterdata:
                acluster.add(self.getNode(nodedata[0]))
            _clusters.append(acluster)
        for servicename in servicesdata.keys():
            atype = servicesdata[servicename]['type']
            nodeids = servicesdata[servicename]['nodes']
            #nodes = [self.getNode(id) for id in nodeids]
            nodes = {}
            for resId in nodeids:
                anode = self.getNode(resId)
                anode.allocated = servicename
                nodes[resId] = anode
            classname = Fabric.svctype[atype] + 'Service'
            
            aservice = eval(classname)(servicename, nodes)
            if aservice.load_config(self._moveConf):  # Load configuration to contact remote sites
                aservice.setLogger(self.logger)  # include log descriptor
                aservice.setVerbose(self.verbose)  # enable print on the screen
                #aservice.setTeefaa(self.teefaaobj)
            else:
                msg = "Loading configuration of the Service " + str(aservice.identifier) + ". The service will not be included. " + \
                                  " Please add service configuration in the fg-server.conf file under a section called Move-<service>-<site> (i.e. Move-eucalyptus-sierra)"
                self.logger.error(msg)
                print "ERROR: " + msg
            
            _services.append(aservice)
        
        return _nodes, _services
      
    def load(self, inventory):
        '''load data from inventory to bootstrap the fabric'''
        #print inventory.__class__.__name__
        self._inventory = inventory
        data = self._inventory.read()
        if self.verbose:
            print data
        else:
            self.logger.debug(str(data))
        _nodes = []
        _clusters = []
        _services = []
        nodesdata = data['nodes']
        clustersdata = data['clusters']
        servicesdata = data['services']
        for node in nodesdata:
            _nodes.append(Node(node[0],node[1],node[2],node[3]))
        self.updateNodes(_nodes)
        for clustername in clustersdata.keys():
            acluster = Cluster(clustername)
            clusterdata = clustersdata[clustername]
            for nodedata in clusterdata:
                acluster.add(self.getNode(nodedata[0]))
            _clusters.append(acluster)
        for servicename in servicesdata.keys():
            atype = servicesdata[servicename]['type']
            nodeids = servicesdata[servicename]['nodes']
            #nodes = [self.getNode(id) for id in nodeids]
            nodes = {}
            for resId in nodeids:
                anode = self.getNode(resId)
                anode.allocated = servicename
                nodes[resId] = anode
            classname = Fabric.svctype[atype] + 'Service'
            
            aservice = eval(classname)(servicename, nodes)
            if aservice.load_config(self._moveConf):  # Load configuration to contact remote sites
                aservice.setLogger(self.logger)  # include log descriptor
                aservice.setVerbose(self.verbose)  # enable print on the screen
                #aservice.setTeefaa(self.teefaaobj)
            else:
                msg = "Loading configuration of the Service " + str(aservice.identifier) + ". The service will not be included. " + \
                                  " Please add service configuration in the fg-server.conf file under a section called Move-<service>-<site> (i.e. Move-eucalyptus-sierra)"
                self.logger.error(msg)
                print "ERROR: " + msg
            
            _services.append(aservice)
        self.update(_nodes,_clusters,_services)
        return

    def store(self):
        '''data persistence after new update'''
        data = {"clusters": self.getCluster(), "services":self.getService()}
        self._inventory.write(data)
        
    def getNode(self, identifier=None):
        '''get a node based on the identifier, or return all nodes if id not provided'''
        if identifier is not None:
            if self._nodes.has_key(identifier):
                ret = self._nodes[identifier]
            else:
                ret = None
                #print "Node does not exist"
        else:
            ret = self._nodes
        return ret
        
    def getCluster(self, identifier=None):
        '''get a cluster based on the identifier, or return all clusters if id not provided'''
        if identifier is not None:
            if self._clusters.has_key(identifier):
                ret = self._clusters[identifier]
            else:
                ret = None
                #print "Node does not exist"
        else:
            ret = self._clusters
        return ret
        
    def getService(self, identifier=None):
        '''get a service based on the identifier, or return all services if id not provided'''
        if identifier is not None:
            if self._services.has_key(identifier):
                ret = self._services[identifier]
            else:
                ret = None
                #print "Node does not exist"
        else:
            ret = self._services
        return ret
    
    def addNode(self, node):
        '''Add a Node to the node dict
           cluster is the id of the cluster where the node is'''
        self._nodes[node.identifier]=node
        
        #store in the DB
        self._inventory.addNode2Cluster(node)
        
    def addCluster(self, cluster):
        '''Add a Cluster to the cluster dict'''
        self._clusters[cluster.identifier]=cluster
        
        #store in the DB
        self._inventory.createCluster(cluster.identifier)   #this is not needed in MongoDB, but I put it just in case we decide 
                                                            # to use another DB later.
        
    def addService(self, service):
        '''Add a Service to the service dict'''
        success=True
        msg='OK'
        if service.load_config(self._moveConf):  # Load configuration to contact remote sites
            service.setLogger(self.logger)  # include log descriptor
            service.setVerbose(self.verbose)  # enable print on the screen
            #service.setTeefaa(self.teefaaobj)
            self._services[service.identifier]=service
            
            try:
                self._inventory.createService(service.identifier, service.type) #this is not needed in MongoDB, but I put it just in case we decide 
                                                                            # to use another DB later.
            except:
                msg = "ERROR: Storing Service in the Database. " + str(sys.exc_info())
                self.logger.error(msg)
                success=False
            
        else:            
            msg = "Loading configuration of the Service " + str(service.identifier) + ". The service will not be included. " + \
                              " Please add service configuration in the fg-server.conf file under a section called Move-<service>-<site> (i.e. Move-eucalyptus-sierra)"
            self.logger.error(msg)
            success=False
        
        return success, msg
    
    def addNode2Service(self, nodeId,service):
        self._inventory.addNode2Service(nodeId, service.identifier, service.type)
        
    def removeNodeFromService(self, nodeId, service):
        self._inventory.removeNodeFromService(nodeId, service.identifier, service.type)
       
    def update(self, nodes=(), clusters=(), services=()):
        '''update the nodes, clusters, and services data'''
        self.updateNodes(nodes)
        self.updateClusters(clusters)
        self.updateServices(services)
        if self.verbose:
            print "updating inventory...."
            print self._inventory
            print "just printed the inventory of the fabric"
        else:
            self.logger.debug("updating inventory....")
        #if self._inventory is not None:
        #    self.store()
           
    def updateNodes(self, nodes=()):
        '''update the nodes list'''
        self._nodes = dict()
        for node in nodes:
            key = node.identifier
            self._nodes[key] = node
            
    def updateClusters(self, clusters=()):
        '''update the clusters data'''
        self._clusters = dict()
        for cluster in clusters:
            key = cluster.identifier
            self._clusters[key] = cluster
        
    def updateServices(self, services=()):
        '''update the services data'''
        self._services = dict()
        for service in services:
            key = service.identifier
            self._services[key] = service
                        
    def info(self):
        '''info of the fabric - identifiers of all nodes, clusters, and services'''
        nodes = "Nodes:\n" + ",".join(sorted(self._nodes.keys()))
        clusters = "Clusters:\n" + ",".join(sorted(self._clusters.keys()))
        services = "Services:\n" + ",".join(sorted(self._services.keys()))
        return nodes + "\n" + clusters + "\n" + services + "\n"
        
    def __repr__(self):
        return self.info()
