from futuregrid_move.rain.move.Resource import Resource, Node, Cluster, Service

class HPCService(Service):
    def __init__(self, resId, res=dict()):
        
        super(HPCService, self).__init__()
        
        self._id = resId
        self._type = "HPC"
        self._res = res

    #doadd and doremove have been moved to the Resources.py in the Service class. So this class inherit those methods
    """
    def doadd(self, ares): #This is the same in all the classes. We should move it to the father
        success = False
        
        msg = "INSIDE " + self._type + "Service:doadd: add into " + self._type + " service"
        self.logger.debug(msg)
        if self.verbose:
            print msg
        
        msg = "Calling Teefaa provisioning"
        self.logger.debug(msg)
        if self.verbose:
            print msg
            
        status = self.teefaaobj.provision(ares.name, self._type, ares.cluster)        
        
        if status != 'OK':
            self.logger.error(status)
            if self.verbose:
                print status
            success = False
        else:
            msg = "Teefaa provisioned the host " + ares.name + " of the site " + ares.cluster + " with the os " + self._type + " successfully"
            self.logger.debug(msg)
            if self.verbose:
                print msg
                    
            msg = "Calling RainMoveSite to ensure the node is active in the service"
            self.logger.debug(msg)
            if self.verbose:
                print msg
            
            connection=self.socketConnection()
            if connection != None:
                connection.write(self._type + ", add, " + ares.name)
                status = connection.read(1024)
                self.socketCloseConnection(connection)
                if status == "OK":
                    success = True
                else:
                    success = False
                    self.logger.error(status)
                    if self.verbose:
                        print status                
            else:
                msg = "ERROR: Connecting with the remote site. The node was not allocated to the service."
                self.logger.error(msg)
                if self.verbose:
                    print msg        
        
        return success

    def doremove(self, ares): #This is the same in all the classes. We should move it to the father
        success = False
        
        msg = "INSIDE " + self._type + "Service:doremove: remove from " + self._type + " service"
        self.logger.debug(msg)
        if self.verbose:
            print msg
        
        connection=self.socketConnection()
        if connection != None:
            connection.write(self._type + ", remove, " + ares.name)
            status = connection.read(1024)
            self.socketCloseConnection(connection)
            
            if status == "OK":
                success = True
            else:
                success = False
                self.logger.error(status)
                if self.verbose:
                    print status       
        else:
            msg = "ERROR: Connecting with the remote site. The node was not removed."
            self.logger.error(msg)
            if self.verbose:
                print msg
        
        return success
    """
    def cbadd(self, ares):
        print "INSIDE HPCService:cbadd: Added " + ares.identifier + " to service " + self.identifier
        return

    def cbremove(self, ares):
        print "INSIDE HPCService:cbremove: Removed " + ares.identifier + " from service " + self.identifier
        return
