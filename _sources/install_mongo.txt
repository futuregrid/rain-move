.. _chap_install_mongodb:


Deployment of MongoDB
=====================

In this section we are going to explain how to install a single MongoDB service. More information can be found in `MongoDB <http://www.mongodb.org/>`_

.. note::
      In MongoDB the databases and tables are created automatically.
      
      Remember that MongoDB is case sensitive.

.. _mongodb:

Install MongoDB
---------------

* Download the package file for you specific distribution. They can be found in http://www.mongodb.org/downloads.

* Uncompress the file.

    :: 
    
      tar cvfz <filename>
      
* Create DB directory

   ::
   
      sudo mkdir -p /data/db/
      sudo chown `id -u` /data/db     #The owner must be the user that is going to execute mongodb server
      
* Run MongoDB

   ::
   
      mongod --port 23000 --dbpath /data/db/ --fork --logpath=/data/db/mongo.log
      
      
* Test MongoDB using the client.

   ::
   
      $ mongo --port 23000

      > db.foo.save ( {a:1} )
      > db.foo.find ()

.. _pymongo:

Install pymongo
---------------

The latest documentation can be found in http://api.mongodb.org/python/2.3rc1/installation.html.

* Install with pip

   ::

      pip install pymongo

* Install with easy_install

   ::
   
      easy_install install pymongo