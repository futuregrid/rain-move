.. _quickstart:

FG Move QuickStart
==================

Requirements
------------

At this moment, our software only provides command line interfaces. Thus, users need access to the machine where the client part of the 
software is installed. Currently, this is installed and configured in the India cluster (``india.futuregrid.org``). 
  
Login on India and use the module functionality to load the environment variables:

   ::

      $ ssh <username>@india.futuregrid.org
      $ module load futuregrid

.. note::
   At this point, FG Move is only available for administrators.


The authentication is done via FutureGrid Ldap server. Thus, in each command we need to specify our FutureGrid username and we 
will be asked for our portal password 

   ::

      $ fg-move -u <username> ...

.. note::
   Users need to use their FutureGrid username and portal password.

Using FG Move
-------------

The command line of this service is organized in three specialized subparsers.

* ``node``. A node is the representation of a physical machine. This subparses exposes the functionality to operate with them.

* ``cluster``. A cluster is a set of nodes identified by a name. This subparser exposes the functionality to operate with them.

* ``service``. A service is the representation of an infrastructure, which is composed by nodes. It exposes the functionality to operate with them (move, add, delete, list nodes)

Operating with Clusters
+++++++++++++++++++++++

* Create a cluster named Indiana

  ::

    fg-move -u jdiaz cluster --create Indiana

* List available clusters

  ::

    fg-move -u jdiaz cluster --list
    
* List information of a particular cluster

  ::

    fg-move -u jdiaz cluster --list Indiana     
    
Operating with Nodes
++++++++++++++++++++

* Add a node to a particular cluster. We need to indicate the properties of the node. They are identified of the node, hostname, IP and the cluster.

  ::

    fg-move -u jdiaz node --add i90.india i90 10.0.1.2 Indiana

* List information of a particular node.

  ::

    fg-move -u jdiaz cluster --info i90.india

Operating with Services
+++++++++++++++++++++++

* Create a service named IndianaOpenStack.

  ::

    fg-move -u jdiaz service --create IndianaOpenStack

* List available services.

  ::

    fg-move -u jdiaz service --list

* List information of a particular service.

  ::

    fg-move -u jdiaz service --list IndianaOpenStack

* List nodes that are not assigned to any service.

  ::

    fg-move -u jdiaz service --listfreenodes


* Add nodes to the service. The nodes cannot be assigned to another service, that is they must be free.

  ::

    fg-move -u jdiaz service --add i90.india i20.india IndianaOpenStack
     
* Remove a node from a service. The node must be idle to perform this operation. You can force by adding ``--force``.

  ::

    fg-move -u jdiaz service --remove i20.india IndianaOpenStack
   
* Move a node from a service to another. The node must be idle to perform this operation. You can force by adding ``--force``. 

  ::

    fg-move -u jdiaz service --move i90.india IndianaOpenStack IndianaEucalyptus

