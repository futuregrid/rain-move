from Resource import Resource, Node, Cluster, Service

class HPCService(Service):
    def __init__(self, id, res=dict()):
        self._id = id
        self._type = "HPC"
        self._res = res

    def doadd(self, ares):
        print "INSIDE HPCService:doadd: To be implemented: add into HPC service"
        return True

    def doremove(self, ares):
        print "INSIDE HPCService:cbremove: To be implemented: remove from HPC service"
        return True

    def cbadd(self, ares):
        print "INSIDE HPCService:cbadd: Added " + ares.identifier + " to service " + self.identifier
        return

    def cbremove(self, ares):
        print "INSIDE HPCService:cbremove: Removed " + ares.identifier + " from service " + self.identifier
        return
