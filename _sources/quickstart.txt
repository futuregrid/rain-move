.. _quickstart:

FG Move QuickStart
==================

Requirements
------------

At this moment, our software only provides a command line interface. Thus, users need access to the machine where the FG Move client 
is installed. Currently, this is installed and configured in the FutureGrid India cluster (``india.futuregrid.org``). 
  
Login on India and use the module functionality to load the environment variables:

   ::

      $ ssh <username>@india.futuregrid.org
      $ module load futuregrid

.. note::
   FG Move is only available for administrators.


The authentication is done via FutureGrid Ldap server. Thus, in each command we need to specify our FutureGrid username and we 
will be asked for our portal password. After the user is successfully authenticated against the Ldap server, it is verified if that user
is authorized to use the FG Move service.   

   ::

      $ fg-move -u <username> ...

.. note::
   Users need to use their FutureGrid username and portal password.

Using FG Move
-------------

The command line of this service is organized in three specialized subparsers.

* **node**. A node is the representation of a physical machine. This subparses exposes the functionality to operate with them.

* **cluster**. A cluster is a set of nodes identified by a name (representation of a physical cluster). This subparser exposes the 
  functionality to operate with them.

* **service**. A service is the representation of an infrastructure, which is composed by nodes. It exposes the functionality to move
  physical machines from one infrastructure to another.

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

* Add a node to a particular cluster. We need to indicate the properties of the node, which are a node ID, hostname, 
  IP and cluster ID.

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

* List nodes that are not allocated into any service.

  ::

    fg-move -u jdiaz service --listfreenodes


* Add nodes to the service IndianaOpenStack. The nodes must be free, that is they cannot be allocated to another service.

  ::

    fg-move -u jdiaz service --add i90.india i20.india IndianaOpenStack
     
* Remove a node from a service. The node must be idle to perform this operation or you have to force the opration by adding ``--force``.

  ::

    fg-move -u jdiaz service --remove i20.india IndianaOpenStack
   
* Move a node from a service to another. The node must be idle to perform this operation or you have to force the opration by adding ``--force``.

  ::

    fg-move -u jdiaz service --move i90.india IndianaOpenStack IndianaEucalyptus

