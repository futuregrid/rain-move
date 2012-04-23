from Resource import Resource, Node, Cluster, Service

class EucaService(Service):
    def __init__(self, id, res=dict()):
        self._id = id
        self._type = "Eucalyptus"
        self._res = res

    def doadd(self, ares):
        print "INSIDE EucaService:doadd: To be implemented: add into Euca service"
        return True

    def doremove(self, ares):
        print "INSIDE EucaService:cbremove: To be implemented: remove from Euca service"
        return True

    def cbadd(self, ares):
        print "INSIDE EucaService:cbadd: Added " + ares.identifier + " to service " + self.identifier
        return

    def cbremove(self, ares):
        print "INSIDE EucaService:cbremove: Removed " + ares.identifier + " from service " + self.identifier
        return
