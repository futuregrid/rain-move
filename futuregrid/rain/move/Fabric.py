"""
The Fabric module

"""

__author__ = 'Fugang Wang'
__version__ = '0.1'

import abc
import json
import re
from Resource import Resource, Node, Cluster, Service
from EucaService import EucaService
from OpenStackService import OpenStackService
from NimbusService import NimbusService
from HPCService import HPCService

class Inventory(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def read(self):
        return
    
    @abc.abstractmethod
    def write(self):
        return

class InventoryFile(Inventory):
    
    def __init__(self, fname):
        self._cfgfile = fname
        self._res = dict()
        return
    
    def read(self):
        file = open(self._cfgfile)
        content = file.read()
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
                        id = m.group(1)
                        name = m.group(2)
                        ip = m.group(3)
                        #print id, name, ip
                        nodes.append([id,name,ip,clustername])
                        current.append([id,name,ip,clustername])
                        
                    #node list for service in format of: identifier
                    else:
                        nodeidregex = re.compile('(.+)')
                        m = nodeidregex.match(line)
                        if m is not None:
                            id = m.group(1)
                            current.append(id)
                        else:
                            print "ERROR"
                    #print line
        ret = {"nodes":nodes, "clusters":clusters, "services":services}
        #print ret
        return ret
    
    def write(self):
        return

class InventoryDB(Inventory):
    
    def __init__(self, config):
        return
    
    def read(self):
        return
    
    def write(self):
        return
                    
class Fabric(object):
    svctype = {'hpc':'HPC', 'eucalyptus':'Euca', 'nimbus':'Nimbus', 'openstack':'OpenStack'}
    def __init__(self, nodes=(), clusters=(), services=()):
        self.update(nodes, clusters, services)
            
    def load(self, inventory):
        #print inventory.__class__.__name__
        data = inventory.read()
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
            for id in nodeids:
                anode = self.getNode(id)
                anode.allocated = servicename
                nodes[id] = anode
            classname = Fabric.svctype[atype] + 'Service'
            aservice = eval(classname)(servicename, nodes)
            _services.append(aservice)
        self.update(_nodes,_clusters,_services)
        return
    
    def getNode(self, identifier=None):
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
        if identifier is not None:
            if self._services.has_key(identifier):
                ret = self._services[identifier]
            else:
                ret = None
                #print "Node does not exist"
        else:
            ret = self._services
        return ret
        
    def update(self, nodes=(), clusters=(), services=()):
        self.updateNodes(nodes)
        self.updateClusters(clusters)
        self.updateServices(services)
           
    def updateNodes(self, nodes=()):
        self._nodes = dict()
        for node in nodes:
            key = node.identifier
            self._nodes[key] = node
            
    def updateClusters(self, clusters=()):
        self._clusters = dict()
        for cluster in clusters:
            key = cluster.identifier
            self._clusters[key] = cluster
        
    def updateServices(self, services=()): 
        self._services = dict()
        for service in services:
            key = service.identifier
            self._services[key] = service
                        
    def info(self):
        nodes = "Nodes:\n" + ",".join(sorted(self._nodes.keys()))
        clusters = "Clusters:\n" + ",".join(sorted(self._clusters.keys()))
        services = "Services:\n" + ",".join(sorted(self._services.keys()))
        return nodes + "\n" + clusters + "\n" + services + "\n"
        
    def __repr__(self):
        return self.info()
