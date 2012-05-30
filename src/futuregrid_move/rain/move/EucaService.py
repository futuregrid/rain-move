from futuregrid_move.rain.move.Resource import Resource, Node, Cluster, Service

class EucaService(Service):
    def __init__(self, resId, res=dict()):
        super(EucaService, self).__init__()
        
        self._id = resId
        self._type = "Eucalyptus"
        self._res = res
        

    def doadd(self, ares):
        print "INSIDE EucaService:doadd: To be implemented: add into Euca service"\
        
        connection=self.socketConnection()
        if connection != None:
            connection.write(self._type + ", add, " + ares.identifier)
            print connection.read(1024)
        else:
            print "ERROR: Connecting with the remote site. UNDO if we added changed the node in the DB or Try again."
        self.socketCloseConnection(connection)
        
        return True

    def doremove(self, ares):
        print "INSIDE EucaService:cbremove: To be implemented: remove from Euca service"
        connection=self.socketConnection()
        if connection != None:
            connection.write(self._type + ", remove, " + ares.identifier)
            print connection.read(1024)
        else:
            print "ERROR: Connecting with the remote site. UNDO if we added changed the node in the DB or Try again."
        self.socketCloseConnection(connection)
        return True

    def cbadd(self, ares):
        print "INSIDE EucaService:cbadd: Added " + ares.identifier + " to service " + self.identifier
        return

    def cbremove(self, ares):
        print "INSIDE EucaService:cbremove: Removed " + ares.identifier + " from service " + self.identifier
        return
