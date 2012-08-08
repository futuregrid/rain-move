.. _chap_whatis:


What is FutureGrid Move?
========================

Summary
-------

FutureGrid Move is a service that enables physical resources re-allocation among infrastructures. By using a simple command line interface,
this service is able to de-register a machine from a particular infrastructure and register it in another one. Internally, this service 
makes use of `Teefaa <http://futuregrid.github.com/teefaa/>`_ to dynamically provision the selected machine with the OS and software 
needed for a successful registration in the new infrastructure. FG Move also maintains a database with information about the machines 
composing each one of the different infrastructures. The database can be consulted to obtain detailed information 
about a particular infrastructure.

An scheduler will be created to integrate FG Move with our metric `FutureGrid Metrics <https://portal.futuregrid.org/metrics/html/index.html>`_. In this
way, it will allow us to make reservations or analyze the historical usage to automatically move resources according to user demand.  


The following picture represents the architecture of FG Move.

.. image:: fg-move_all.png
   :align: center
   :height: 350 px
   :width: 600 px

The workflow that "moves" a machine from one infrastructure to another is the following:

* The client requests to move a resource.
* FG Move Server contacts with the FG Move Controller of the original infrastructure to de-register the machine.
   * If the machine is idle, it is de-registered.
   * If the machine is not idle, it waits for the machine to became idle (for a certain amount of time) or it terminates all its tasks/VMs. 
     Then, the machine is de-registered.
* FG Move Server calls Teefaa to provision the machine with the appropriated OS. Teefaa will repartition the disk of the machine and place the
  required OS.
* FG Move Server contacts with the FG Move Controller of the destination infrastructure to register the machine.

Currently, we support HPC infrastructures (Torque-based) and cloud infrastructures based on `Eucalyptus <http://open.eucalyptus.com/>`_ 
and `OpenStack <http://www.openstack.org>`_ frameworks. Additionally, we are working to provide support to other cloud infrastructures based 
on `Nimbus <http://www.nimbusproject.org>`_ and `OpenNebula <http://www.opennebula.org>`_ frameworks.


Use Cases
---------

* Re-allocate machines based on user demands. This can be initiated by creating a reservation, by predicting future needs (learning 
  for historical information), or manually.

* Conduct tests on the same machines with different frameworks.

* Re-use images created for experiments.


