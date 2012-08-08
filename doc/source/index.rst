Welcome to FuturGrid Move
=========================

FutureGrid Move is a service that enables physical resources re-allocation among infrastructures. By using a simple command line interface,
this service is able to de-register a machine from a particular infrastructure and register it in another one. Internally, this service 
makes use of `Teefaa <http://futuregrid.github.com/teefaa/>`_ to dynamically provision the selected machine with the OS and software 
needed for a successful registration in the new infrastructure. FG Move also maintains a database with information about the machines 
composing each one of the different infrastructures. The database can be consulted to obtain detailed information 
about a particular infrastructure.

Currently, we support HPC infrastructures (Torque-based) and cloud infrastructures based on `Eucalyptus <http://open.eucalyptus.com/>`_ 
and `OpenStack <http://www.openstack.org>`_ frameworks. Additionally, we are working to provide support to other cloud infrastructures based 
on `Nimbus <http://www.nimbusproject.org>`_ and `OpenNebula <http://www.opennebula.org>`_ frameworks.

.. toctree::
    :maxdepth: 1
    :hidden:
    
    whatis
    quickstart
    documentation
    download
    support


.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`

