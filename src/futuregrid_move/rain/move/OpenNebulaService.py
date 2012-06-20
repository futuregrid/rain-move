from futuregrid_move.rain.move.Resource import Resource, Node, Cluster, Service

class OpenNebulaService(Service):
    def __init__(self, resId, res=dict()):
        
        super(OpenNebulaService, self).__init__()
        
        self._id = resId
        self._type = "OpenNebula"
        self._res = res

    #doadd and doremove have been moved to the Resources.py in the Service class. So this class inherit those methods
    """
    def doadd(self, ares):
        print "INSIDE OpenNebulaService:doadd: To be implemented: add into OpenNebula service"
        
        print "Calling Teefaa provisioning"
        status = self.teefaaobj.provision(ares.identifier, self._type, ares.cluster)        
        
        if status != 'OK':
            print status
        else:
            print "Teefaa provisioned the host " + ares.identifier + " of the site " + ares.cluster + " with the os " + self._type + " successfully"
        
        print "Calling RainMoveSite to ensure the node is active in the service"
        
        connection=self.socketConnection()
        if connection != None:
            connection.write(self._type + ", add, " + ares.identifier)
            print connection.read(1024)
        else:
            print "ERROR: Connecting with the remote site. UNDO if we added changed the node in the DB or Try again."
        self.socketCloseConnection(connection)
        
        return True

    def doremove(self, ares):
        print "INSIDE OpenNebulaService:cbremove: To be implemented: remove from OpenNebula service"
        
        connection=self.socketConnection()
        if connection != None:
            connection.write(self._type + ", remove, " + ares.name)
            print connection.read(1024)
        else:
            print "ERROR: Connecting with the remote site. UNDO if we added changed the node in the DB or Try again."
        self.socketCloseConnection(connection)
        
        return True
    """
    def cbadd(self, ares):
        print "INSIDE OpenNebulaService:cbadd: Added " + ares.identifier + " to service " + self.identifier
        return

    def cbremove(self, ares):
        print "INSIDE OpenNebulaService:cbremove: Removed " + ares.identifier + " from service " + self.identifier
        return
