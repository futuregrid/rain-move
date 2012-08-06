Welcome to FuturGrid Move
=========================

FutureGrid Move is a service that enables physical resources re-allocation among infrastructures. By using a simple command line interface,
this service is able to de-register a machine from a particular infrastructure and register it in a new one. Internally, this service 
makes use of `Teefaa <http://futuregrid.github.com/teefaa/>`_ to dynamically provision the selected machine with the OS and software 
needed for a successful registration in the new infrastructure. FG Move also maintains a database with information about the machines 
composing each one of the different infrastructures, which can be queried to consult the current status or detailed information about
a particular infrastructure.

Currently, we support HPC (Torque), `Eucalyptus <http://open.eucalyptus.com/>`_ and `OpenStack <http://www.openstack.org>`_ infrastructures.
However, we are working to provide support to `Nimbus <http://www.nimbusproject.org>`_ and `OpenNebula <http://www.opennebula.org>`_ infrastructures.


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

