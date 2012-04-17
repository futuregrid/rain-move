The documentation is at 

http://futuregrid.github.com/rain-move

=================

The following notes will be moved into that documentation directory.

here are my initial thoughts on fg move

the way i think we can do this is to introduce a number of trivial datastructures and than just manage them for each cluster and stick them into an overall datastructure cluster (possibly we rename this to cotton as i am in doubt about the word cluster and we may have other things than clusters in future).

we would than write "providers" that allows us to add a particular service to the framework while implementing some of the methods that are initially not defined. 

we may have a service directory in which we have classes that call out the native service APIs that do some of the functinality, such as registering and deregistering a node with the services and so forth.

I did not share this with anyone but you and like to get your input today.

If possible I like to get a first implementation on this by next week and write a paper on it.

I think we can ask Koji to look into the hpc related scripts, you and Fugang could do OpenStack/OpenNebula/Nimbus/Eucalyptus

I am not sure how free Koji is for this however. If we can not use Koji, we can simulate ths with the SLURM virtual clusters in some way at least for HPC ;-)

#This class may be renamed to cotton.

#euclyptus
#nimbus
#openstack
#opennebula
#hpc
#...

class Clusters:
    # manages all services on a variety of clusters

""" 
fabric> define cluster india

fabric> set cluster india

fabric> add i136.india.futuregrid.org

   #resource will be added. information about ip, memory, and disks will
   #be automatically discovered, either from a file, or via login

fabric> set cluster sierra

fabric> add s136 eucalyptus 24GB 500GB s136.sierra.futuregrid.org 
#   ip address wil be identified based on hostname

...

"""



class Resources:
    def add(name, type=None, memory, disk, hostname=None, ip=None):
        return

    def assign(name, hostname, ip):
        return

    def getinfo(hostname):
        #sets all discoverable values of the given hostname, memory,
        #disk, ip, the name is the first part of the hostname
        retrun

    def setinfo(name, type=None, memory, disk, hostname=None, ip=None):
        # overwrites the given info for the resource with the given name

    def match (regexp):
        #returns the resources that match the regular expression on the name
        return

    def _matchByHostname(regexp):
        #returns the resources that match the regular expression on
        #the hostname
        return

class Service:

    string name = None

    def __init__(type,version):
        return

    def add(resources): 
        return

    def addNode (resource):
        return

   def removeNode (resource):
        return

    def _rain(name):
        # rains the specified service onto the resource. Internally
        # used by addNode
    
    def list(): # print
        return

class Services:
    services = {}

    def add (service):
        return

    def remove (service):
        return

    def list(): #print
        return

    def write(filename):
        return

    def read(filename):

# we will have an pool with reources that can be used for backfilling


class shell:
"""
A CMD2 shell in which we can issue a number of commands. 

fabric> list

  lists all resources and services in the fabric

fabric> list resources

  lists the resources

fabric> list services

  lists the services

fabric> list name

  lists the object with the name 

SERVICE COMMANDS

fabric> suspend name

  suspends the service with the name
  
fabric> resume name

  resumes the service with the name

fabric> reset name

  resets the service with the name

RAIN COMMANDS

fabric> rain resource-name service-name

  deploys a service on the named resource
  the command move internally calls rain

fabric> move resource-name service-name

  moves or adds the named resource to the named service if the
  resource was used elswhere, move will also derigister orderly the
  old service

fabric> kill resource-name

  kills all services on the named resource


IP COMMANDS

fabric> getIP

  returns a free IP

fabric> getIP from to

  returns a free IP between the given range

fabric> getIP resource-name

  gets a free ip and assigns it to the named resource

fabric> releaseIP resource-name

  releases the IP of the resource

"""
    return

and many more ....