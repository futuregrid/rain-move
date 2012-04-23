#!/usr/bin/env python

from Resource import Resource, Node, Cluster, Service
from HPCService import HPCService
from EucaService import EucaService
from OpenStackService import OpenStackService
from NimbusService import NimbusService
from Fabric import Fabric, Inventory, InventoryFile, InventoryDB

def main():
    print "\n------Typing TEST---"
    print Resource.TYPE
    #will not work - cannot instantiate abstract class
    #res = Resource.Resource()
    node = Node("testnode")
    print node
    print "node identifier: " + node.identifier
    print "node type: " + node.type
    node.ip="123.123.123.123"
    print node.ip
    node.ip="123.123.123.000"
    print node.ip

    print "\n------Cluster testing..."
    print "---Empty cluster..."
    india = Cluster("india")
    print india.list()
    print "---Adding a node..."
    india.add(Node("i136.india.futuregrid.org","i136"))
    print india.list()
    print "---Adding another node..."
    india.add(Node("i100.india.futuregrid.org","i100","149.165.146.100"))
    print india.list()
    print "---Another cluster..."
    hotel = Cluster("hotel", (Node("i01.hotel.futuregrid.org"), Node("i02.hotel.futuregrid.org")))
    print hotel.list()
    print "---Adding a node..."
    hotel.add(Node("i10.hotel.futuregrid.org"))
    print hotel.list()
    print "---Adding another node..."
    hotel.add(Node("i20.hotel.futuregrid.org"))
    print hotel.list()

    
    print "\n------Service testing..."
    print "---initiate an HPC  service..."
    indiahpc = HPCService("HPC on India")
    print "service identifier: " + indiahpc.identifier
    print "service type: " + indiahpc.type
    print "---initiate more services..."
    indiaeuca = EucaService("Eucalyptus on India")
    indiaopenstack = OpenStackService("OpenStack on India")
    hotelnimbus = NimbusService("Nimbus on Hotel")
    print "service identifier: " + indiaeuca.identifier
    print "service type: " + indiaeuca.type
    print "service identifier: " + indiaopenstack.identifier
    print "service type: " + indiaopenstack.type
    print "service identifier: " + hotelnimbus.identifier
    print "service type: " + hotelnimbus.type
    print "---add a free node to HPC ..."
    node1 = Node("i88.india.futuregrid.org")
    indiahpc.add(node1)
    print indiahpc.list()
    print "---add a free node to Euca ..."
    node1e = Node("i66.india.futuregrid.org")
    indiaeuca.add(node1e)
    print indiaeuca.list()
    print "---add another node to HPC ..."
    node2 = Node("i99.india.futuregrid.org")
    indiahpc.add(node2)
    print indiahpc.list()
    print "---add an occupied node to Euca ..."
    indiaeuca.add(node2)
    print indiaeuca.list()
    print "---add an occupied node to HPC..."
    indiahpc.add(node1e)
    print indiahpc.list()
    print "---status of node2..."
    print node2
    print "---remove a node..."
    indiahpc.remove(node2.identifier)
    print indiahpc.list()
    print "---status of node2 after removed from service..."
    print node2
    print "---remove an unexisting node..."
    indiahpc.remove(node1e.identifier)
    print indiahpc.list()
    print "---status of node1e after being tried to be removed from service HPC..."
    print node1e
    
    print "\n------Fabric testing..."
    fg = Fabric()
    print fg
    fg = Fabric((node1, node2),(india, hotel),(indiahpc,indiaeuca))
    print fg
    #inv = InventoryFile("testinv")
    #fg.load(inv)
    #invnew = InventoryDB("testinv2")
    #fg.load(invnew)
    print fg.getNode().keys()
    print fg.getNode("i88.india.futuregrid.org")
    print fg.getNode("i66.india.futuregrid.org")
    print fg.getService().keys()
    invreal = InventoryFile("FGResInventory")
    fg.load(invreal)
    print fg.info()
    
if __name__ == "__main__":
    main()
