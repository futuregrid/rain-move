Welcome to FuturGrid Move Project
======================

FutureGrid move deals with moving resources between multiple clouds
and HPC services in a multicluster, multisite deployment.

Assume you have a number of nodes in a cluster and what one day to use
them for you r HPC services, but the next day as part of your cloud
environment, or you want to move resources between different version
of your cloudinstalation such as Opensatck Bexar and Essex.

You can do this with::

  fg-move -h <list of hosts> deactivate

This will deactivate the ndes from the list and put them into a pool
of available resources. To provide the state of the host you can use::

  fg-move -h <list of hosts> -status

For convenience you can create a group of hosts that are registered to
a label::

  fg-vgroup -h <list of hosts> -label <label> 


This will allow you to replace the hostlist with a group command with
the -g option::

  fg-move -g <groupname> status

The last gommand lists the status of all nodes in that group. To
activate a service for that host, you simply specify::

  fg-move -h <hostlist> -service <servicename>

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

  fg-move -g myEucalyptusCloud -h node1.machine.edu, node2.machine.edu
  fg-move -activate "eucalyptus" -v "3.0" -g myEucalyptusCloud

Would provide a eucalyptus cloud with the node1 and node2 from
machine.edu. The EUcalyptus zone name is tacken from the group name.







Provides a status of the hosts. 








  




Within FutureGrid we provide a number of devellopment projects. This
page is used to provide you with easy links to them. All projects
listed are managed in github.

Projects
============

Code related to FutureGrid

Rain
  * A project to do bare metal and VM based dynamic provisioning
  * Documentation: http://futuregrid.github.com/rain
  * Source: https://github.com/futuregrid/rain

Cloud Shift
  * A project to move resources between different cloud and HPC services
  * Documentation: todo
  * Source: todo
  * Issues: todo

Cloud Metric
  * A project to measure and display metric information about usage and utilization of your cloud 
  * Documentation: https://portal.futuregrid.org/doc/metric/index.html
  * Source: https://github.com/futuregrid/futuregrid-cloud-metrics
  * Issues: https://github.com/futuregrid/futuregrid-cloud-metrics/issues
..  Documentation: https://futuregrid.github.com/futuregrid-cloud-metrics

Virtual Cluster
  * A project to create a SLURM based cluster in your cloud and run MPI jobs on it
  * Documentation: http://futuregrid.github.com/virtual-cluster
  * Source: https://github.com/futuregrid/virtual-cluster
  * Issues: https://github.com/futuregrid/virtual-cluster/issues

Authentication
  * A project to unify authentication between Eucalyptus, OpenStack, and Nimbus
  * Documentation: todo
  * Source: todo
  * Issues: todo

Mediawiki Jira Issues
  * A project that can be used to automatically create reports based on comments submitted to jira, returning jira issues in mediawiki, and executing arbitrary queries from mediawiki to jira that are rendered in mediawiki
  * Documentation: todo
  * Source: todo
  * Issues: todo


.. toctree::
   :maxdepth: 2

.. todo   intro

.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`

