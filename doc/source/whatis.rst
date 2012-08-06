.. _chap_whatis:


What is FutureGrid Move?
========================

Summary
-------

FutureGrid Move is a service that enables physical resources re-allocation among infrastructures. By using a simple command line interface,
this service is able to de-register a machine from a particular infrastructure and register it in a new one. Internally, this service 
makes use of `Teefaa <http://futuregrid.github.com/teefaa/>`_ to dynamically provision the selected machine with the OS and software 
needed for a successful registration in the new infrastructure. FG Move also maintains a database with information about the machines 
composing each one of the different infrastructures, which can be queried to consult the current status or detailed information about
a particular infrastructure.

This service will create an scheduler to integrate the `FutureGrid Metrics <https://portal.futuregrid.org/metrics/html/index.html>`_. In this
way, it will allow us to make reservations or analyze the historical usage to automatically move resources according to user demand.  


The following picture represents the architecture of FG Move.

.. image:: fg-move_all.png
   :align: center
   :scale: 60 %


Currently, we support HPC infrastructures (Torque-based) and cloud infrastructures based on `Eucalyptus <http://open.eucalyptus.com/>`_ 
and `OpenStack <http://www.openstack.org>`_ frameworks. Additionally, we are working to provide support to other cloud infrastructures based 
on `Nimbus <http://www.nimbusproject.org>`_ and `OpenNebula <http://www.opennebula.org>`_ frameworks.




Use Cases
---------

* Re-assign machines based on user demands. This can be initiated manually, by creating a reservation or by predicting future needs (learning 
for historical information).

* Conduct tests on the same machines with different frameworks.

* Re-use images created for experiments


