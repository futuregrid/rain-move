.. _man-move:

Move (fg-move)
==============

FG Move is a service to re-allocate resources among infrastructures.

General Usage
-------------

::

   usage: fg-move [-h] -u user {node,cluster,service} ...

   
   positional arguments: 
             {node,cluster,service}  Positional arguments group different options 
                                     that can be displayed by specifying <positional_argument> -h
   

+--------------------------+---------------------------------------------------------------------------------+
| **Option**               | **Description**                                                                 |
+--------------------------+---------------------------------------------------------------------------------+
| ``-h/--help``            | Shows help information and exit.                                                |
+--------------------------+---------------------------------------------------------------------------------+
| ``-u/--user <userName>`` | FutureGrid HPC user name, that is, the one used to login into the FG resources. |
+--------------------------+---------------------------------------------------------------------------------+

Node subparser
--------------

::

   usage: fg-move -u user node [-h] (-a nodeId hostname ip cluster | -r nodeId cluster | -i nodeId ) [-f]
   
   Options between brackets are not required. Parenthesis means that you need to specify one of the options.   

+-----------------------------------------------------------------------------------------+-------------------------------------------------------------------------------+
| **Option**                                                                              | **Description**                                                               |
+-----------------------------------------------------------------------------------------+-------------------------------------------------------------------------------+
| ``-h/--help``                                                                           | Shows help information and exit.                                              |
+-----------------------------------------------------------------------------------------+-------------------------------------------------------------------------------+
| ``-a <nodeId> <hostname> <ip> <clusterId>, --add <nodeId> <hostname> <ip> <clusterId>`` | Add new node to a cluster.                                                    |
+-----------------------------------------------------------------------------------------+-------------------------------------------------------------------------------+
| ``-r <nodeId> <clusterId>, --remove <nodeId> <clusterId>``                              | Remove node. It is also removed from cluster and service. (not supported yet) |
+-----------------------------------------------------------------------------------------+-------------------------------------------------------------------------------+
| ``-i <nodeId>, --info <nodeId>``                                                        | Information of a node.                                                        |
+-----------------------------------------------------------------------------------------+-------------------------------------------------------------------------------+
| ``-f, --force``                                                                         | Force operation.                                                              |
+-----------------------------------------------------------------------------------------+-------------------------------------------------------------------------------+


Examples
--------

* Add a node to a particular cluster. We need to indicate the properties of the node, which are a node ID, hostname, 
  IP and cluster ID.

  ::

    fg-move -u jdiaz node --add i90.india i90 10.0.1.2 Indiana

* List information of a particular node.

  ::

    fg-move -u jdiaz cluster --info i90.india


Cluster subparser
-----------------

::

   usage: fg-move -u user cluster [-h] (-c clusterId | -r clusterId | -l [clusterId]) [-f]

   
   Options between brackets are not required. Parenthesis means that you need to specify one of the options.   

+------------------------------------------+-----------------------------------------------------------------------------------------------+
| **Option**                               | **Description**                                                                               |
+------------------------------------------+-----------------------------------------------------------------------------------------------+
| ``-h/--help``                            | Shows help information and exit.                                                              |
+------------------------------------------+-----------------------------------------------------------------------------------------------+
| ``-c <clusterId>, --create <clusterId>`` | Create a new cluster.                                                                         |
+------------------------------------------+-----------------------------------------------------------------------------------------------+
| ``-r <clusterId>, --remove <clusterId>`` | Remove cluster (not supported yet)                                                            |
+------------------------------------------+-----------------------------------------------------------------------------------------------+
| ``-l [clusterId], --list [clusterId]``   | List available clusters or the information about a particular one if a clusterId is provided. |
+------------------------------------------+-----------------------------------------------------------------------------------------------+
| ``-f, --force``                          | Force operation.                                                                              |
+------------------------------------------+-----------------------------------------------------------------------------------------------+


Examples
--------

* Create a cluster named Indiana

  ::

    fg-move -u jdiaz cluster --create Indiana

* List available clusters

  ::

    fg-move -u jdiaz cluster --list
    
* List information of a particular cluster

  ::

    fg-move -u jdiaz cluster --list Indiana  
    

Service subparser
-----------------

::

   usage: fg-move -u user service [-h] (-c serviceId type | -a nodeId/s... [nodeId/s...] serviceId | -r nodeId/s... [nodeId/s...] serviceId 
                              | -m nodeId/s... [nodeId/s...] serviceIdorigin serviceIddestination | -l [serviceId] | -s [clusterId])
                          [-f]


   Options between brackets are not required. Parenthesis means that you need to specify one of the options.   

+---------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
| **Option**                                                                      | **Description**                                                                                        |
+---------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
| ``-h/--help``                                                                   | Shows help information and exit.                                                                       |
+---------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
| ``-c/--create <serviceId>``                                                     | Create a new service.                                                                                  |
+---------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
| ``-a/--add <nodeId/s> [nodeId/s...] <serviceId>``                               | Add a node or list of nodes to a service.                                                              |
+---------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
| ``-r/--remove <nodeId/s> [nodeId/s...] <serviceId>``                            | Remove a node or list of nodes from a service.                                                         |
+---------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
| ``-m/--move <nodeId/s> [nodeId/s...] <serviceIdorigin> <serviceIddestination>`` | Move a node or list of nodes from a service to another.                                                |
+---------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
| ``-l/--list [serviceId]``                                                       | List available services or the information about a particular one if a clusterId is provided.          |
+---------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
| ``-s/--listfreenodes [clusterId]``                                              | List of nodes that are not assigned to any service. The list can be restricted to a particular cluster |
+---------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
| ``-f/--force``                                                                  | Force operation.                                                                                       |
+---------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------+


Examples
--------

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

