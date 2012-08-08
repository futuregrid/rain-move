.. _chap_configure_futuregrid-move:

Setting up the FutureGrid Software for FG Move
==============================================

Configuration Files
-------------------

There are two places where we can locate the configuration files. Our software will look into these places in the following order:   

#. In the directory ``~/.fg/``
#. In the directory ``/etc/futuregrid/`` 

If you have installed FutureGrid Move using the tarball file (:ref:`Using a source tarball <source_tarball>`) you will find the configuration 
sample files in /etc/futuregrid/. Otherwise, you can download them as a :docs-tar:`tarball <configsamples>` or a :docs-zip:`ZIP file <configsamples>`.

**Server Side**: The configuration file has to be renamed as ``fg-server.conf``.

**Client Side**: The configuration file has to be renamed as ``fg-client.conf``. 

.. note::
   If you configure several clients or servers in the same machine, the ``fg-client.conf`` or ``fg-server.conf`` must be the same file.

.. note::
   In the **Client Side**, the path of the log files must be relative to each users. Using the ``$HOME`` directory is a good idea.

Setting up LDAP
---------------

The authentication of our software is based on LDAP. So, we need to configure some options in the configuration files to make it possible. 

Server Side
***********

We need to configure the ``[LDAP]`` section. This is going to be use by all servers. More information about this section 
of the server configuration file can be found in :ref:`LDAP section <fg-server_ldap>`.

   .. highlight:: bash

   ::
   
      [LDAP]
      LDAPHOST= ldap.futuregrid.org
      LDAPUSER= uid=rainadmin,ou=People,dc=futuregrid,dc=org
      LDAPPASS= passwordrainadmin
      log= ~/fg-auth.log




Setting up FG Move
------------------

In this section we explain how to configure FG Move. FG Move is composed by a main server that orchestrates different FG Move controllers 
distributed among the different infrastructures head nodes. There controllers make sure that the machines are properly added or removed
from the infrastructure.

.. _move_config:

Server Side
***********

First, we are going to configure the main server. We need to configure the ``[RainMoveServer]`` Section 
(see :ref:`MoveServer section <fg-server_rainmoveserver>`). 

   .. highlight:: bash

   ::
   
      [RainMoveServer]
      port = 56795
      proc_max=5
      refresh=20
      authorizedusers = adminuser1, adminuser2
      log = moveserver.log
      log_level = debug
      ca_cert=/opt/futuregrid/futuregrid/etc/imdserver/cacert.pem
      certfile=/opt/futuregrid/futuregrid/etc/imdserver/imdscert.pem
      keyfile=/opt/futuregrid/futuregrid/etc/imdserver/privkey.pem
      Clientca_cert=/opt/futuregrid/futuregrid/etc/imdclient/cacert.pem
      Clientcertfile=/opt/futuregrid/futuregrid/etc/imdclient/imdccert.pem
      Clientkeyfile=/opt/futuregrid/futuregrid/etc/imdclient/privkey.pem

.. _move_sites_sections:

Next we need to create sections for each one of the FG Move controllers (see :ref:`Move Remote Site Controllers<fg-server_move_remote_sites_example>`).


   .. highlight:: bash

   ::

      [Move-eucalyptus-indiaeuca]
      address=129.79.49.12
      port=56804
      
      [Move-openstack-indiaopenstack]
      address=129.79.49.13
      port=56805
      
      [Move-hpc-indiahpc]
      address=129.79.49.10
      port=56806
      
      [Move-nimbus-hotelnimbus]
      address=129.79.49.11
      port=56807

.. note::

   Make sure that ``port`` and ``address`` matches with those used by the Move controllers (see :ref:`Move Site Server <move_sites_server>`).

We also have to create an inventory file that will describe the nodes, clusters and services. This file will be read by the RainMoveServer
during its initialization. The nodes are defined by its Id, hostname and IP. They have to be part of a cluster, which is defined by the 
label **CLUSTER:** followed by the name of the cluster. 

 This file looks like:

   .. highlight:: bash

   ::

      [CLUSTER:HOTEL]
      c01.hotel,c01,149.165.147.1
      c02.hotel,c02,149.165.147.2
      
      [CLUSTER:INDIA]
      i01.india,i01,149.165.148.1
      i02.india,i02,149.165.148.2
      i100.india,i200,149.165.148.100
      i101.india,i101,149.165.148.101
      i102.india,i102,149.165.148.102
      
      [SERVICE:NIMBUS:HOTELNIMBUS]
      c01.hotel
      c02.hotel
      
      [SERVICE:EUCALYPTUS:INDIAEUCA]
      i100.india
      i102.india
      
      [SERVICE:OPENSTACK:INDIAOPENSTACK]
      i101.india
      
      [SERVICE:HPC:INDIAHPC]
      i01.india
      i02.india



This server requires to have `Teefaa <http://futuregrid.github.com/teefaa/>`_ installed in the same 
machine (see `Teefaa Documentation <http://futuregrid.github.com/teefaa/documentation.html>`_).

Once everything is set up (including Teefaa), you can start the server executing ``RainMoveServer.py -l <inventoryfile>`` as ``imageman`` user.

.. note::
   We recommend to have a system user that run all the servers (i.e. imageman). In this way, it will be easier to manage the sudoers file when necessary. 

.. _move_client_conf:

Client Side
***********

In the client side, we need to configure the ``[RainMove]`` section. More information 
about this section of the client configuration file can be found in :ref:`Move section <fg-client_move>`.

   .. highlight:: bash

   ::
     
      [RainMove]
      port = 56796
      proc_max = 5
      refresh = 20
      log = movesiteserver.log
      log_level = debug
      max_wait = 1000
      ec2varfile = ~/eucarc
      ca_cert=/etc/futuregrid/imdserver/cacert.pem
      certfile=/etc/futuregrid/imdserver/imdscert.pem
      keyfile=/etc/futuregrid/imdserver/privkey.pem
     
Once you have everything set up, any user that is in the ``authorizedusers`` field of the section ``[RainMoveServer]`` will be able to
use this service (see :ref:`Rain Move Server <move_config>`). Of course, the user has to authenticate against LDAP too. 

The executable file of this client is ``fg-move``. More information about how to use FG Move can be found in the :ref:`FG Move Manual <man-move>`.


FG Move Check List
******************

+-----------------+-----------------------------------------------------------------+----------------------------------+
|                 | Server Side (``fg-server.conf``)                                | Client Side (``fg-client.conf``) |
+=================+=================================================================+==================================+
| **Requirement** | - Teefaa installed and configured in the same machine           |                                  |
+-----------------+-----------------------------------------------------------------+----------------------------------+
| **Configure**   | - ``[RainMoveServer]`` section                                  | - ``[RainMove]`` section         |
|                 | - ``[LDAP]`` section                                            |                                  |
|                 | - Move Site controllers sections ``Move-<service>-<serviceID>`` |                                  |
+-----------------+-----------------------------------------------------------------+----------------------------------+
| **Executables** | - ``RainMoveServer.py``                                         | - ``fg-move``                    |
+-----------------+-----------------------------------------------------------------+----------------------------------+


.. _move_sites_server:

Setting up FG Move Site Controller
----------------------------------

In this section, we explain how to configure the FG Move Site Controller. As we said previously, this service will make sure that the machines 
are properly added or removed from the infrastructure. Therefore, it has to run in the machine that controls the infrastructure 
(i.e. where Torque, OpenStack Nova manager or Eucalyptus cloud controller is installed). Our service controller is generic and works for 
every supported infrastructure, we only need to tune it up properly.

Server Side
***********

In the Server side we need to configure the ``[RainMoveSiteServer]`` Section (see :ref:`RainMoveSiteServer section <fg-server_rainmoveserver>`). 

   .. highlight:: bash

   ::
   
      [RainMoveSiteServer]
      port = 56796
      proc_max = 5
      refresh = 20
      log = movesiteserver.log
      log_level = debug
      max_wait = 1000
      ec2varfile = ~/eucarc
      ca_cert=/etc/futuregrid/imdserver/cacert.pem
      certfile=/etc/futuregrid/imdserver/imdscert.pem
      keyfile=/etc/futuregrid/imdserver/privkey.pem

.. note::

   Make sure that the ``port`` specified here matches with the one specified in the sections defined when configuring the main :ref:`FG Move server <move_sites_sections>`. 

Next, we need to do specific configurations depending on the infrastructure we are targeting. Typically, you only need to do one of the following
subsections per management machine.

* **HPC infrastructure**

 Considering that ``imageman`` is the user that will run the service, we need to allow this user to execute the ``pbsnodes`` command and some 
 other commands as ``root`` user. 
 
 Edit ``sudoers`` file by executing ``visudo`` as ``root`` user and add the following lines:
   
   ::
  
      Defaults    secure_path = /sbin:/bin:/usr/sbin:/usr/bin:/opt/moab/bin:/opt/torque/bin
      
      imageman ALL=(ALL) NOPASSWD: /opt/moab/bin/mschedctl -R
      imageman ALL=(ALL) NOPASSWD: /opt/torque/bin/pbsnodes 
      imageman ALL=(ALL) NOPASSWD: /opt/torque/bin/qmgr
      imageman ALL=(ALL) NOPASSWD: /opt/torque/bin/qdel

  .. note: 
     The ``ec2varfile`` field of the section  ``[RainMoveSiteServer]`` described previously is not used in this service.

* **Eucalyptus Infrastructure**

  Here, we need to provide ``imageman`` with an Eucalyptus credentials of an admin user. This is basically needed to terminate instances when
  we use the ``--force`` option with fg-move. A good place to place the creadentials is the home directory of this user.

  Next, we need to edit ``sudoers`` file by executing ``visudo`` as ``root`` user and add the following lines:

   ::
  
      Defaults    secure_path = /sbin:/bin:/usr/sbin:/usr/bin:/opt/euca/bin
      
      imageman ALL=(ALL) NOPASSWD: /opt/euca/bin/euca_conf
      

* **OpenStack Infrastructure**

  Here, we need to provide ``imageman`` with an OpenStack credentials of an admin user. This is basically needed to terminate instances when
  we use the ``--force`` option with fg-move. A good place to place the creadentials is the home directory of this user.

  Next, we need to edit ``sudoers`` file by executing ``visudo`` as ``root`` user and add the following lines:

   ::
  
      Defaults    secure_path = /sbin:/bin:/usr/sbin:/usr/bin:/opt/openstack/bin
      
      imageman ALL=(ALL) NOPASSWD: /opt/openstack/bin/nova-manage


* **Nimbus Infrastructure**
   
   Not developed yet

* **OpenNebula Infrastructure**
   
   Not developed yet 


Once everything is set up, you can start the server by execution ``RainMoveSiteServer.py`` as ``imageman`` user.

FG Move Site Check List
***********************

+-----------------+-----------------------------------------------------------+
|                 | Server Side (``fg-server.conf``)                          |
+=================+===========================================================+
| **Access to**   | - Cloud credentials of an admin user (not needed for HPC) |
+-----------------+-----------------------------------------------------------+
| **Configure**   | - ``[RainMoveSiteServer]`` section                        |
|                 | - sudoers                                                 |
+-----------------+-----------------------------------------------------------+
| **Executables** | - ``RainMoveSiteServer.py``                               |
+-----------------+-----------------------------------------------------------+
