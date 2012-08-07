Welcome to FuturGrid Move Project
======================

FutureGrid move deals with moving resources between multiple clouds
and HPC services in a multicluster, multisite deployment.

Assume you have a number of nodes in a cluster and what one day to use
them for you r HPC services, but the next day as part of your cloud
environment, or you want to move resources between different version
of your cloudinstalation such as Opensatck Bexar and Essex.

You can do this with::

  fg-fabric -h <list of hosts> deactivate

This will deactivate the ndes from the list and put them into a pool
of available resources. To provide the state of the host you can use::

  fg-fabric -h <list of hosts> -status

For convenience you can create a group of hosts that are registered to
a label::

  fg-vgroup -h <list of hosts> -label <label> 


This will allow you to replace the hostlist with a group command with
the -g option::

  fg-fabric -g <groupname> status

The last gommand lists the status of all nodes in that group. To
activate a service for that host, you simply specify::

  fg-fabric -h <hostlist> -service <servicename>

The service names are requstered with our framework and correspond to
specific actions to be taken to activate and deacivate nodes from this
service.

We will support the following services:

* eucalyptus
* openstack
* nimbus
* opennebula
* hpc 

A version cnd a cluster name can be optionally provided. Thus the
commands::

  fg-fabric -g myEucalyptusCloud -h node1.machine.edu, node2.machine.edu
  fg-fabric -activate "eucalyptus" -v "3.0" -g myEucalyptusCloud-service myEucalyptusCloud

Would provide a eucalyptus cloud with the node1 and node2 from
machine.edu. The Eucalyptus zone name is tacken from the group name.

Usecase 1: Adding more nodes to a cloud

Assume you have the group 

  indiaEuclyptusCloud that contains node[1-4].machine.edu

You like to add the machines node[5-9].machine.edu. This can be done via::

  fg-fabric -g newNodes -h node[5-9].machine.edu
  fg-fabric -g newNodes -service indiaEucalyptus 







