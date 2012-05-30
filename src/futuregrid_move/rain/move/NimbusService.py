from futuregrid_move.rain.move.Resource import Resource, Node, Cluster, Service

class NimbusService(Service):
    def __init__(self, resId, res=dict()):
        
        super(NimbusService, self).__init__()
        
        self._id = resId
        self._type = "Nimbus"
        self._res = res
        
        

    def doadd(self, ares):
        print "INSIDE NimbusService:doadd: To be implemented: add into Nimbus service"
        
        connection=self.socketConnection()
        if connection != None:
            connection.write(self._type + ", add, " + ares.identifier)
            print connection.read(1024)
        else:
            print "ERROR: Connecting with the remote site. UNDO if we added changed the node in the DB or Try again."
        self.socketCloseConnection(connection)
        
        return True

    def doremove(self, ares):
        print "INSIDE NimbusService:cbremove: To be implemented: remove from Nimbus service"
        
        connection=self.socketConnection()
        if connection != None:
            connection.write(self._type + ", remove, " + ares.identifier)
            print connection.read(1024)
        else:
            print "ERROR: Connecting with the remote site. UNDO if we added changed the node in the DB or Try again."
        self.socketCloseConnection(connection)
        
        return True

    def cbadd(self, ares):
        print "INSIDE NimbusService:cbadd: Added " + ares.identifier + " to service " + self.identifier
        return

    def cbremove(self, ares):
        print "INSIDE NimbusService:cbremove: Removed " + ares.identifier + " from service " + self.identifier
        return
