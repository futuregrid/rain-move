.. _sec_fg-server.conf:

``fg-server.conf`` configuration file
-------------------------------------

.. _fg-server_ldap:

Section ``[LDAP]``
******************

This section is used to configure the access to LDAP to verify the user passwords.

*This section is required by all services*

Option ``LDAPHOST``
~~~~~~~~~~~~~~~~~~~

**Type:** String

**Required:** Yes

Hostname or IP address of the LDAP server that manages the user's authentication.

Option ``LDAPUSER``
~~~~~~~~~~~~~~~~~~~

**Type:** user-dn

**Required:** Yes

This is the DN of an user that have read access to the encrypted passwords of every user. This looks 
like ``uid=USER,ou=People,dc=futuregrid,dc=org`` 

Option ``LDAPPASS``
~~~~~~~~~~~~~~~~~~~

**Type:** String

**Required:** Yes

Password of the user specified in the previous section.

Option ``log``
~~~~~~~~~~~~~~

**Type:** log-file

**Required:** Yes

Location of the file where the logs will be stored.

Option ``test``
~~~~~~~~~~~~~~~

**Valid values:** ``True``, ``False``

**Required:** No

This option is for development purposes. For security reasons, the LDAP server cannot be contacted from outside of FutureGrid network.
Therefore, we need this option to go test our services before we deploy them on production.

****************

.. _fg-server_rainmoveserver:

Section ``[RainMoveServer]``
****************************

This section is used to configure the FG Move Server. 

Option ``port``
~~~~~~~~~~~~~~~

**Type:** Integer

**Required:** Yes

Port where the FG Move server will be listening.

Option ``proc_max``
~~~~~~~~~~~~~~~~~~~

**Type:** Integer

**Required:** Yes

Maximum number of request that can be processed at the same time.

Option ``refresh``
~~~~~~~~~~~~~~~~~~

**Type:** Integer

**Required:** Yes

Interval to check the status of the running requests when ``proc_max`` is reached and determine if new request can be processed.

Option ``authorizedusers``
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Type:** String-list (comma separated)

**Required:** No

List of users (separated by commas) that can use this service.

.. Option ``nopasswdusers``
.. ~~~~~~~~~~~~~~~~~~~~~~~~

.. **Type:** Dictionary-list (semicolon separated) 

.. **Required:** No

.. Users listed here does need to introduce their password when using the Image Repository. Each user will be associated to one or several 
.. IP address. The format is ``userid:ip,ip1; userid1:ip2,ip3``.

Option ``log``
~~~~~~~~~~~~~~

**Type:** log-file

**Required:** Yes

Location of the file where the logs will be stored.

Option ``log_level``
~~~~~~~~~~~~~~~~~~~~

**Valid values:** ``debug``, ``error``, ``warning``, ``info``

**Required:** No

Desired log level. The default option is ``debug``.

Option ``ca_cert``
~~~~~~~~~~~~~~~~~~

**Type:** ca-cert

**Required:** Yes

Location of CA certificate (PEM-encoded) used to generate user and service certificates. Server certificates.

Option ``certfile``
~~~~~~~~~~~~~~~~~~~

**Type:** service-cert

**Required:** Yes

Location of the certificate (PEM-encoded) used by the FG Move server. Server certificates.

Option ``keyfile``
~~~~~~~~~~~~~~~~~~

**Type:** key-cert

**Required:** Yes

Location of the private key (PEM-encoded) of the certificate specified in ``certfile``. Server certificates.

Option ``Clientca_cert``
~~~~~~~~~~~~~~~~~~~~~~~~

**Type:** ca-cert

**Required:** Yes

Location of CA certificate (PEM-encoded) used to generate user and service certificates. Client certificates.

Option ``Clientcertfile``
~~~~~~~~~~~~~~~~~~~~~~~~~

**Type:** service-cert

**Required:** Yes

Location of the certificate (PEM-encoded) used by the FG Move server to contact with the Move site controllers. Client certificates.

Option ``Clientkeyfile``
~~~~~~~~~~~~~~~~~~~~~~~~

**Type:** key-cert

**Required:** Yes

Location of the private key (PEM-encoded) of the certificate specified in ``certfile``. Client certificates.


****************

.. _fg-server_move_remote_sites_example:

Sections ``[Move-<service>-<serviceID>]`` such as ``[Move-eucalyptus-indiaeuca]`` or ``[Move-Hpc-indiahpc]``
************************************************************************************************************

This sections are to define how to contact the remove site controllers (``RainMoveSiteServer.py`` server)

Option ``address``
~~~~~~~~~~~~~~~~~~

**Type:** String

**Required:** Yes

Address of the server where FG Move site server will be running.

Option ``port``
~~~~~~~~~~~~~~~

**Type:** Integer

**Required:** Yes

Port where the FG Move site server will be listening.

****************


.. _fg-server_rainmovesiteserver:

Section ``[RainMoveSiteServer]``
********************************

This section is used to configure the FG Move Site Server, which is the FG Move controller place in the management machines. 

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

Option ``port``
~~~~~~~~~~~~~~~

**Type:** Integer

**Required:** Yes

Port where the FG Move server will be listening.

Option ``proc_max``
~~~~~~~~~~~~~~~~~~~

**Type:** Integer

**Required:** Yes

Maximum number of request that can be processed at the same time.

Option ``refresh``
~~~~~~~~~~~~~~~~~~

**Type:** Integer

**Required:** Yes

Interval to check the status of the running requests when ``proc_max`` is reached and determine if new request can be processed.

Option ``log``
~~~~~~~~~~~~~~

**Type:** log-file

**Required:** Yes

Location of the file where the logs will be stored.

Option ``log_level``
~~~~~~~~~~~~~~~~~~~~

**Valid values:** ``debug``, ``error``, ``warning``, ``info``

**Required:** No

Desired log level. The default option is ``debug``.

Option ``ec2varfile``
~~~~~~~~~~~~~~~~~~~~~

**Type:** EC2-file

**Required:** (Only for Cloud infrastructures)

Location of the EC2 environment variable file, which typically is eucarc or novarc.  

Option ``ca_cert``
~~~~~~~~~~~~~~~~~~

**Type:** ca-cert

**Required:** Yes

Location of CA certificate (PEM-encoded) used to generate user and service certificates. Server certificates.

Option ``certfile``
~~~~~~~~~~~~~~~~~~~

**Type:** service-cert

**Required:** Yes

Location of the certificate (PEM-encoded) used by the FG Move server. Server certificates.

Option ``keyfile``
~~~~~~~~~~~~~~~~~~

**Type:** key-cert

**Required:** Yes

Location of the private key (PEM-encoded) of the certificate specified in ``certfile``. Server certificates.