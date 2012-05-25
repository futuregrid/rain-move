from Resource import Resource, Node, Cluster, Service

class OpenStackService(Service):
    def __init__(self, id, res=dict()):
        
        super(OpenStackService, self).__init__()
        
        self._id = id
        self._type = "OpenStack"
        self._res = res

    def doadd(self, ares):
        print "INSIDE OpenStackService:doadd: To be implemented: add into OpenStack service"
        
        connection=self.socketConnection()
        if connection != None:
            connection.write(self._type + ", add, " + ares.identifier)
            print connection.read(1024)
        else:
            print "ERROR: Connecting with the remote site. UNDO if we added changed the node in the DB or Try again."
        self.socketCloseConnection(connection)
        
        return True

    def doremove(self, ares):
        print "INSIDE OpenStackService:cbremove: To be implemented: remove from OpenStack service"
        
        connection=self.socketConnection()
        if connection != None:
            connection.write(self._type + ", remove, " + ares.identifier)
            print connection.read(1024)
        else:
            print "ERROR: Connecting with the remote site. UNDO if we added changed the node in the DB or Try again."
        self.socketCloseConnection(connection)
        
        return True

    def cbadd(self, ares):
        print "INSIDE OpenStackService:cbadd: Added " + ares.identifier + " to service " + self.identifier
        return

    def cbremove(self, ares):
        print "INSIDE OpenStackService:cbremove: Removed " + ares.identifier + " from service " + self.identifier
        return
