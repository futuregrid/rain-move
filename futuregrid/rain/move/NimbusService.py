from Resource import Resource, Node, Cluster, Service

class NimbusService(Service):
    def __init__(self, id):
        self._id = id
        self._type = "Nimbus"
        self._res = dict()

    def doadd(self, ares):
        print "INSIDE NimbusService:doadd: To be implemented: add into Nimbus service"
        return True

    def doremove(self, ares):
        print "INSIDE NimbusService:cbremove: To be implemented: remove from Nimbus service"
        return True

    def cbadd(self, ares):
        print "INSIDE NimbusService:cbadd: Added " + ares.identifier + " to service " + self.identifier
        return

    def cbremove(self, ares):
        print "INSIDE NimbusService:cbremove: Removed " + ares.identifier + " from service " + self.identifier
        return