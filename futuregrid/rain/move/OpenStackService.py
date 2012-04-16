from Resource import Resource, Node, Cluster, Service

class OpenStackService(Service):
    def __init__(self, id):
        self._id = id
        self._type = "OpenStack"
        self._res = dict()

    def doadd(self, ares):
        print "INSIDE OpenStackService:doadd: To be implemented: add into OpenStack service"
        return True

    def doremove(self, ares):
        print "INSIDE OpenStackService:cbremove: To be implemented: remove from OpenStack service"
        return True

    def cbadd(self, ares):
        print "INSIDE OpenStackService:cbadd: Added " + ares.identifier + " to service " + self.identifier
        return

    def cbremove(self, ares):
        print "INSIDE OpenStackService:cbremove: Removed " + ares.identifier + " from service " + self.identifier
        return