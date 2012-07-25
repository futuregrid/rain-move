#!/usr/bin/env python
# -------------------------------------------------------------------------- #
# Copyright 2010-2011, Indiana University                                    #
#                                                                            #
# Licensed under the Apache License, Version 2.0 (the "License"); you may    #
# not use this file except in compliance with the License. You may obtain    #
# a copy of the License at                                                   #
#                                                                            #
# http://www.apache.org/licenses/LICENSE-2.0                                 #
#                                                                            #
# Unless required by applicable law or agreed to in writing, software        #
# distributed under the License is distributed on an "AS IS" BASIS,          #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.   #
# See the License for the specific language governing permissions and        #
# limitations under the License.                                             #
# -------------------------------------------------------------------------- #
"""
Description: Server to do the real operations in the machines. Install software in machine and add/remove from infrastructure.
"""
__author__ = 'Javier Diaz'

from types import *
import re
import logging
import logging.handlers
import random
from random import randrange
import os
import sys
import socket, ssl
from multiprocessing import Process
from subprocess import *
import time
import boto
import boto.ec2

from futuregrid_move.rain.move.RainMoveServerConf import RainMoveServerConf

class RainMoveServerSites(object):

    def __init__(self):
        super(RainMoveServerSites, self).__init__()
        
               
        self.numparams = 4
        

        #load from config file
        self._rainSitesConf = RainMoveServerConf()
        self._rainSitesConf.load_moveSiteServerConfig() 
        
        self.port = self._rainSitesConf.getMoveSitePort()
        self.proc_max = self._rainSitesConf.getMoveSiteProcMax()
        self.refresh_status = self._rainSitesConf.getMoveSiteRefreshStatus()
        self.log_filename = self._rainSitesConf.getMoveSiteLog()
        self.logLevel = self._rainSitesConf.getMoveSiteLogLevel()
        self.service_max_wait = self._rainSitesConf.getMovesiteMaxWait()
        self.ec2varfile = self._rainSitesConf.getMoveSiteEc2varfile()
        
        self._ca_certs = self._rainSitesConf.getMoveSiteServerCaCerts()
        self._certfile = self._rainSitesConf.getMoveSiteServerCertFile()
        self._keyfile = self._rainSitesConf.getMoveSiteServerKeyFile()
        
        
        print "\nReading Configuration file from " + self._rainSitesConf.getConfigFile() + "\n"
        
        self.logger = self.setup_logger("")
        
        
    def setup_logger(self, extra):
        #Setup logging        
        logger = logging.getLogger("RainMoveServerSites" + extra)
        logger.setLevel(self.logLevel)    
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler = logging.FileHandler(self.log_filename)
        handler.setLevel(self.logLevel)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False #Do not propagate to others
        
        return logger

    def start(self):
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', self.port))
        sock.listen(1)
        self.logger.info('Starting Server on port ' + str(self.port))
        
        proc_list = []
        total_count = 0
        while True:        
            if len(proc_list) == self.proc_max:
                full = True
                while full:
                    for i in range(len(proc_list) - 1, -1, -1):
                        #self.logger.debug(str(proc_list[i]))
                        if not proc_list[i].is_alive():
                            #print "dead"                        
                            proc_list.pop(i)
                            full = False
                    if full:
                        time.sleep(self.refresh_status)
            
            total_count += 1
            #channel, details = sock.accept()
            newsocket, fromaddr = sock.accept()
            connstream = 0
            try:
                connstream = ssl.wrap_socket(newsocket,
                              server_side=True,
                              ca_certs=self._ca_certs,
                              cert_reqs=ssl.CERT_REQUIRED,
                              certfile=self._certfile,
                              keyfile=self._keyfile,
                              ssl_version=ssl.PROTOCOL_TLSv1)
                #print connstream                                
                proc_list.append(Process(target=self.process_client, args=(connstream, fromaddr[0])))            
                proc_list[len(proc_list) - 1].start()
            except ssl.SSLError:
                self.logger.error("Unsuccessful connection attempt from: " + repr(fromaddr))
                self.logger.info("Rain Move Site Server Request DONE")
            except socket.error:
                self.logger.error("Error with the socket connection")
                self.logger.info("Rain Move Site Server Request DONE")
            except:
                self.logger.error("Uncontrolled Error: " + str(sys.exc_info()))
                if type(connstream) is ssl.SSLSocket: 
                    connstream.shutdown(socket.SHUT_RDWR)
                    connstream.close() 
                self.logger.info("Rain Move Site Server Request DONE")
    
                
    def process_client(self, connstream, fromaddr):
        
        success = False
        status = "Wrong Operation (default msg)"
        
        start_all = time.time()
        self.logger = self.setup_logger("." + str(os.getpid()))
        self.logger.info('Accepted new connection')
        
        #receive the message
        data = connstream.read(2048)
        self.logger.debug("msg received: " + data)
        params = data.split(',')
        #print data
        #params[0] is service (infrastructure) name.
        #params[1] is the operation
        #params[2] is the operation argument
        #params[3] is to force remove/move
        
        
        service = (params[0].strip()).lower()
        operation = params[1].strip()
        argument = params[2].strip()
        try:
            forcemove = eval(params[3].strip())
        except:
            forcemove = False
        #MORE PARAMETERS ARE NEEDED
        #operation site, infrastructure origin, infrastructure destination, number machines,
        #reinstall?, image source, partitions,
                
        if len(params) != self.numparams and len(params) != self.numparams - 1:
            msg = "ERROR: incorrect message"
            self.errormsg(connstream, msg)
            return

        #DO STUFFS
        #Think if we should created classes for each infrastructure and use polymorphism OR it is easy enough to just use methods.  
        
        if operation == 'add':
            self.logger.debug("Add machine " + argument + " to the service " + service)
            if service == "openstack":
                success, status = self.add_openstack(argument)
            elif service == "eucalyptus":
                success, status = self.add_euca(argument)
            elif service == "hpc":
                success, status = self.add_hpc(argument)
        elif operation == 'remove':
            self.logger.debug("Remove machine " + argument + " from the service " + service)
            if service == "openstack":
                success, status = self.remove_openstack(argument, forcemove)
            elif service == "eucalyptus":
                success, status = self.remove_euca(argument, forcemove)
            elif service == "hpc":
                success, status = self.remove_hpc(argument, forcemove)
        else:
            self.logger.debug("Operation " + operation + " Service " + service + " Argument " + argument)           
        
        if success:  
            self.logger.debug(status)
            connstream.write("OK")
        else:
            self.logger.error(status)
            connstream.write(status)
            
        try:
            connstream.shutdown(socket.SHUT_RDWR)
            connstream.close()
        except:
            self.logger.error("ERROR: " + str(sys.exc_info()))

    def add_hpc(self, hostname):
        exitloop = False
        success = False
        status = "default msg"
        wait = 0
        max_wait = self.service_max_wait / 10
        
        
        #check if exists
        self.logger.debug("checking if the node exists")
        cmd = "pbsnodes " + hostname
        self.logger.debug(cmd)
        p = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)
        std = p.communicate()
        if p.returncode != 0:
            self.logger.debug("The node " + hostname + " is not in the list, we need to add it.")
            
            self.logger.debug("creating node in torque")
            cmd1 = ["sudo", "qmgr", "-c", "create node " + hostname]
            self.logger.debug(cmd1)
            p1 = Popen(cmd1, stdout=PIPE, stderr=PIPE)
            std1 = p1.communicate()
            if p1.returncode != 0:
                status = "ERROR: creating node. " + str(std1[1])
                self.logger.error(status)                        
                success = False
            else:
                success = True
        else:
            self.logger.debug("enabling node in torque")
            cmd1 = "sudo pbsnodes -c " + hostname
            self.logger.debug(cmd1)
            p1 = Popen(cmd1.split(), stdout=PIPE, stderr=PIPE)
            std1 = p1.communicate()
            if p1.returncode != 0:
                status = "ERROR: enabling node. " + str(std1[1])
                self.logger.error(status)                        
                success = False
            else:
                success = True
        if success:
            self.logger.debug("changing properties of the node")
            cmd1 = ["sudo", "qmgr", "-c", "set node " + hostname + " properties = compute"]
            #cmd1="sudo qmgr -c 'set node " + hostname + " properties = compute' "
            self.logger.debug(cmd1)
            p1 = Popen(cmd1, stdout=PIPE, stderr=PIPE)
            std1 = p1.communicate()
            if p1.returncode != 0:
                status = "ERROR: changing properties node. " + str(std1[1])
                self.logger.error(status)                        
                success = False
            else:
                success = True
        
        time.sleep(120) # wait because the machine has to reboot 
        
        if success:
            self.logger.debug("Waiting until the machine is online")
            while not exitloop:
                cmd = "pbsnodes " + hostname
                self.logger.debug(cmd)
                p = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)
                std = p.communicate()
                if p.returncode == 0:
                    status_torque = std[0].split('\n')[1].strip().split('=')[1].strip()
                    if status_torque == 'free' or status_torque == 'job-exclusive':
                        success = True
                        exitloop = True
                        status = 'OK'
                if wait < max_wait:
                    wait += 1
                    time.sleep(10)
                else:
                    exitloop = True
                    success = False
                    status = "ERROR: Timeout. The node " + hostname + " is not active."
        
        if success:
            cmd = "sudo mschedctl -R"
            self.logger.debug(cmd)
            p = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)
            std = p.communicate()
            if p.returncode == 0:
                status = 'OK'
            else:
                status = 'Problems recycling Moab scheduler'
               
        return success, status   

    def add_openstack(self, hostname):
        exitloop = False
        success = False
        status = "default msg"
        wait = 0
        wait2 = 0
        max_wait = self.service_max_wait / 10
        self.logger.debug("Waiting until the machine is accessible")
        while not exitloop:
            cmd = "sudo nova-manage service list --host " + hostname
            self.logger.debug(cmd)
            p = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)
            std = p.communicate()
            if p.returncode != 0:
                status = "ERROR: Listing hosts. " + str(std[1])
                self.logger.error(status)                        
                exitloop = True
                success = False
            else:
                output = std[0].split()
                output = output[6:]
                if len(output) >= 6:                
                    if output[4].strip() == ':-)':        
                        if output[3].strip() == "enabled":
                            self.logger.debug("Node " + hostname + " is active and enabled")
                            exitloop = True
                            success = True
                        elif output[3].strip() == "disabled":
                            self.logger.debug("Node " + hostname + " is active and disabled")
                            self.logger.debug("Enabling None")
                            cmd = "sudo nova-manage service enable " + hostname + " nova-compute"
                            self.logger.debug(cmd)
                            p = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)
                            std = p.communicate()
                            if p.returncode != 0:
                                status = "ERROR: Enabling node " + hostname + ". " + str(std[1])
                                self.logger.error(status)                        
                                exitloop = True
                                success = False
                    else:
                        self.logger.debug("The Node " + hostname + " is not active. We will keep trying.")                        
                        if wait < max_wait:
                            wait += 1
                            time.sleep(10)
                        else:
                            exitloop = True
                            success = False
                            status = "ERROR: Timeout. The node " + hostname + " is not active."
                else:
                    self.logger.debug("The Node " + hostname + " is not in the list. We will keep trying.")                        
                    if wait2 < max_wait:
                        wait2 += 1
                        time.sleep(10)
                    else:
                        exitloop = True
                        success = False
                        status = "ERROR: Timeout. The node " + hostname + " is not in the list."
                        
        return success, status

    def add_euca(self, hostname):
        
        exitloop = False
        success = False
        status = "default msg"
        wait = 0
        max_wait = self.service_max_wait / 10        
        num_notfounds = 0
        
        
        #TODO WHILE with timeout.
        #'nc -zw3 '+ hostname + ' 22'
        
        self.logger.debug("Waiting until the machine is online")
        access = False
        while not access and wait < max_wait:
            
            time.sleep(60)
             
            cmd = "nc -zw3 " + hostname + " 22"                    
            p = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)
            #status = os.waitpid(p.pid, 0)[1]
            std = p.communicate()
            #print std
            #print p.returncode
            if p.returncode == 0:
            #print status                  
            #if status == 0:
                access = True
                self.logger.debug("The machine " + hostname + " seems to be online")    
            else:                
                if wait < max_wait:
                    wait += 1
                    time.sleep(10)
                else:                    
                    status = "Could not get access to the machine " + hostname
                    self._log.error(status)
                    break                    
                
        if access:
            cmd = "sudo euca_conf --register-nodes " + hostname
            self.logger.debug(cmd)
            p = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)
            std = p.communicate()
            if p.returncode != 0:
                status = "ERROR: Registering the node " + hostname + ". " + str(std[1])
                self.logger.error(status)
                exitloop = True
            else:
                self.logger.debug("Node " + hostname + " registered." + std[0])
                #TODO?:Here, we may need to check if the keys are properly propagated
                #Eucalyptus does not have a way to check if the compute-node is OK from the management machine
            
            while not exitloop:    
                self.logger.debug("checking if the node is registered")
                cmd = "sudo euca_conf --list-nodes"
                self.logger.debug(cmd)
                p = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)
                std = p.communicate()
                if p.returncode != 0:
                    status = "ERROR: Listing hosts. " + str(std[1])
                    self.logger.error(status)                        
                    exitloop = True
                    success = False
                else:                
                    output = std[0].split('\n')
                    found = False
                    for entry in output:
                        if '\t' + hostname + '\t' in entry:
                            status = "The node " + hostname + " appears on the list"
                            self.logger.debug(status)
                            exitloop = True
                            found = True
                            success = True
                            num_notfounds = 0
                            break
                    if not found:
                        if num_notfounds == 20: #this is because euca_conf --list-nodes does not return the whole list sometimes
                            exitloop = True
                            success = True    #change to False when euca_conf works properly
                            status = "WARNING: Node " + hostname + " is not found in the host list. It has not been registered properly"
                        else:
                            num_notfounds += 1 
                            time.sleep(2)
                        
        return success, status

    def remove_hpc(self, hostname, forcemove):
        status = "default msg"
        exitloop = False
        wait = 0
        max_wait = self.service_max_wait / 10
        
        
        self.logger.debug("Making node offline")
        cmd = "sudo pbsnodes -o " + hostname
        self.logger.debug(cmd)
        p = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)
        std = p.communicate()
        if p.returncode != 0:
            status = "ERROR: making node offline. " + str(std[1])
            self.logger.error(status)                        
            exitloop = True
            success = False
        
        while not exitloop:
            self.logger.debug("Checking if the node is free")
            cmd = "pbsnodes " + hostname
            self.logger.debug(cmd)
            p = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)
            std = p.communicate()
            if p.returncode != 0:
                status = "ERROR: describing resources node. " + str(std[1])
                self.logger.error(status)                        
                exitloop = True
                success = False
            else:
                if not re.search('^jobs', std[0].split('\n')[5].strip()):                    
                    self.logger.debug("Node " + hostname + " is free. Deleting")
                    cmd = ["sudo", "qmgr", "-c", "delete node " + hostname]
                    #cmd="sudo qmgr -c 'delete node " + hostname + "'"
                    self.logger.debug(cmd)
                    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
                    std = p.communicate()
                    if p.returncode != 0:
                        status = "ERROR: Deleting node. " + str(std[1])
                        self.logger.error(status)                        
                        exitloop = True
                        success = False
                    else:
                        exitloop = True
                        success = True
                elif forcemove:
                    self.logger.debug("Killing jobs")
                    joblist = std[0].split('\n')[5].split('=')[1].split(',')   
                    for i in joblist:
                        job = i.split('/')
                        if len(job) == 2:
                            jobid = job[1].strip()
                            stat = os.system('sudo qdel ' + jobid)
                            if stat != 0:
                                os.system('sudo qdel -p ' + jobid)
                    self.logger.debug("After jobs terminated")
                    time.sleep(5) #allow them some time to change the status   
                else:
                    self.logger.debug("Waiting until free")
                    if wait < max_wait:
                        wait += 1
                        time.sleep(10)
                    else:
                        exitloop = True
                        success = False
                        status = "ERROR: Timeout. The node " + hostname + " is busy. Try to use force move"

        if not success:
            self.logger.debug("Making node online")
            cmd = "sudo pbsnodes -c " + hostname
            self.logger.debug(cmd)
            p = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)
            std = p.communicate()
            if p.returncode != 0:
                status += "\nERROR: making node back online. " + str(std[1])

        return success, status

    def remove_euca(self, hostname, forcemove):
        status = "default msg"
        exitloop = False
        success = False
        wait = 0
        max_wait = self.service_max_wait / 10
        found = False
        num_notfounds = 0
        while not exitloop:
            self.logger.debug("Checking if the node is free")
            cmd = "sudo euca_conf --list-nodes"
            self.logger.debug(cmd)
            p = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)
            std = p.communicate()
            if p.returncode != 0:
                status = "ERROR: describing resources node. " + str(std[1])
                self.logger.error(status)                        
                exitloop = True
                success = False
            else:
                #print std[0]
                output = std[0].split('\n')
                #print output
                listvms = []
                for entry in output:
                    if '\t' + hostname + '\t' in entry:
                        num_notfounds = 0
                        found = True
                        parts = entry.split('\t')
                        if len(parts) < 4:
                            self.logger.debug("Machine " + hostname + " is free. Deregistering...")
                            cmd = "sudo euca_conf --deregister-nodes " + hostname
                            self.logger.debug(cmd)
                            p = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)
                            std = p.communicate()
                            if p.returncode != 0:
                                self.logger.error("ERROR: Deregistering node. " + str(std[1]))                        
                                exitloop = True
                                success = False
                            else:
                                exitloop = True
                                success = True
                        elif(forcemove):
                            for i in range(3, len(parts)):
                                listvms.append(parts[i])
                            self.logger.debug("Killing instances")
                            status = self.terminate_instances(hostname, "eucalyptus", listvms)
                            if status != "OK":
                                self.logger.error(status)                        
                                exitloop = True
                                success = False                
                            self.logger.debug("After terminate instances call")  
                            time.sleep(5)
                        else:
                            self.logger.debug("Waiting until free")
                            if wait < max_wait:
                                wait += 1
                                time.sleep(10)
                            else:
                                exitloop = True
                                success = False
                                status = "ERROR: Timeout. The node " + hostname + " is busy. Try to use force move"
                        break
                if not found and not success:
                    if num_notfounds == 20: #this is because euca_conf --list-nodes does not return the whole list sometimes
                        exitloop = True
                        success = True
                        status = "ERROR: Node " + hostname + " is not found in the host list."
                    else:
                        num_notfounds += 1 
                        time.sleep(2)
                        status = "ERROR: Timeout. The node " + hostname + " is busy. Try to use force move"
                        
        return success, status
                        
    def remove_openstack(self, hostname, forcemove):
        status = "default msg"
        exitloop = False
        wait = 0
        max_wait = self.service_max_wait / 10
        while not exitloop:
            self.logger.debug("Checking if the node is free")
            cmd = "sudo nova-manage service describe_resource " + hostname
            self.logger.debug(cmd)
            p = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)
            std = p.communicate()
            if p.returncode != 0:
                status = "ERROR: describing resources node. " + str(std[1])
                self.logger.error(status)                        
                exitloop = True
                success = False
            else:
                #print std[0]
                output = std[0].split()
                output = output[5:]
                n_instances = int(output[12]) #get value from use_max because use_now takes longer to be updated
                if n_instances == 0:
                    self.logger.debug("Node " + hostname + " is free. Disabling")
                    cmd = "sudo nova-manage service disable " + hostname + " nova-compute"
                    self.logger.debug(cmd)
                    p = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)
                    std = p.communicate()
                    if p.returncode != 0:
                        status = "ERROR: Disabling node. " + str(std[1])
                        self.logger.error(status)                        
                        exitloop = True
                        success = False
                    else:
                        exitloop = True
                        success = True
                elif forcemove:
                    self.logger.debug("Killing instances")
                    status = self.terminate_instances(hostname, "openstack", None)
                    if status != "OK":                        
                        self.logger.error(status)                        
                        exitloop = True
                        success = False                
                    self.logger.debug("After terminate instances call")
                    time.sleep(5) #allow them some time to change the status   
                else:
                    self.logger.debug("Waiting until free")
                    if wait < max_wait:
                        wait += 1
                        time.sleep(10)
                    else:
                        exitloop = True
                        success = False
                        status = "ERROR: Timeout. The node " + hostname + " is busy. Try to use force move"

        return success, status
    
    def terminate_instances(self, hostname, cloudtype, instanceslist):
        try:
            if cloudtype == "openstack":
                path, region, ec2_url = self.openstack(self.ec2varfile)
            elif cloudtype == "eucalyptus":
                path, region, ec2_url = self.euca(self.ec2varfile)
            
        except:
            msg = "ERROR: getting environment variables " + str(sys.exc_info())            
            self.logger.error(msg)                        
            return msg

        endpoint = ec2_url.lstrip("http://").split(":")[0]

        try:  
            region = boto.ec2.regioninfo.RegionInfo(name=region, endpoint=endpoint)
        except:
            msg = "ERROR: getting region information " + str(sys.exc_info())            
            self.logger.error(msg)                        
            return msg
        try:
            connection = boto.connect_ec2(str(os.getenv("EC2_ACCESS_KEY")), str(os.getenv("EC2_SECRET_KEY")), is_secure=False, region=region, port=8773, path=path)
        except:
            msg = "ERROR:connecting to EC2 interface. " + str(sys.exc_info())
            self.logger.error(msg)                        
            return msg

        if cloudtype == "openstack":
            try:
                reservations = connection.get_all_instances() 
                #print str(reservations)
            except:
                msg = "ERROR:getting all instances. " + str(sys.exc_info())
                self.logger.error(msg)                        
                return msg
    
            for r in reservations:
                for i in r.instances:
                    if hostname in str(i.key_name):
                        self.logger.debug("euca_terminate " + i.id) 
                        try:
                            connection.terminate_instances(str(i.id))
                        except:
                            msg = "ERROR: terminating VM. " + str(sys.exc_info())
                            self.logger.error(msg)                        
                            #return msg  #we should not return
                            
        elif cloudtype == "eucalyptus":
            for i in instanceslist:
                self.logger.debug("euca_terminate " + i)
                try:
                    connection.terminate_instances(str(i))
                except:
                    msg = "ERROR: terminating VM. " + str(sys.exc_info())
                    self.logger.error(msg)                        
                    #return msg #we should not return
                    
        return "OK" 


    def euca(self, varfile):
        self.logger.info('Loading Eucalyptus variables')  
        
        euca_key_dir = os.path.dirname(varfile)      
        if euca_key_dir.strip() == "":
            euca_key_dir = "."
        os.environ["EUCA_KEY_DIR"] = euca_key_dir
                    
        #read variables
        f = open(varfile, 'r')
        for line in f:
            if re.search("^export ", line):
                line = line.split()[1]                    
                parts = line.split("=")
                #parts[0] is the variable name
                #parts[1] is the value
                parts[0] = parts[0].strip()
                value = ""
                for i in range(1, len(parts)):
                    parts[i] = parts[i].strip()
                    parts[i] = os.path.expanduser(os.path.expandvars(parts[i]))                    
                    value += parts[i] + "="
                value = value.rstrip("=")
                value = value.strip('"')
                value = value.strip("'") 
                os.environ[parts[0]] = value
        f.close()
            
        
        ec2_url = os.getenv("EC2_URL")
        s3_url = os.getenv("S3_URL")
        
        path = "/services/Eucalyptus"
        region = "eucalyptus"
        
        return path, region, ec2_url
        
        
    def openstack(self, varfile):
        """
        varfile = openstack variable files(novarc typically)
        """
        self.logger.info('Starting Rain Client OpenStack')     
        nova_key_dir = os.path.dirname(varfile)            
        if nova_key_dir.strip() == "":
            nova_key_dir = "."
        os.environ["NOVA_KEY_DIR"] = nova_key_dir
                    
        #read variables
        f = open(varfile, 'r')
        for line in f:
            if re.search("^export ", line):
                line = line.split()[1]                    
                parts = line.split("=")
                #parts[0] is the variable name
                #parts[1] is the value
                parts[0] = parts[0].strip()
                value = ""
                for i in range(1, len(parts)):
                    parts[i] = parts[i].strip()
                    parts[i] = os.path.expanduser(os.path.expandvars(parts[i]))                    
                    value += parts[i] + "="
                value = value.rstrip("=")
                value = value.strip('"')
                value = value.strip("'") 
                os.environ[parts[0]] = value
        f.close()
        
        
        ec2_url = os.getenv("EC2_URL")
        s3_url = os.getenv("S3_URL")
        
        path = "/services/Cloud"
        region = "nova"
        
        return path, region, ec2_url



    def errormsg(self, connstream, msg):
        self.logger.error(msg)
        try:
            connstream.write(msg)
            connstream.shutdown(socket.SHUT_RDWR)
            connstream.close()
        except:
            self.logger.debug("In errormsg: " + str(sys.exc_info()))
        self.logger.info("Rain Move Site Server DONE")
        
def main():

    #Check if we have root privs 
    #if os.getuid() != 0:
    #    print "Sorry, you need to run with root privileges"
    #    sys.exit(1)

    print "\n The user that executes this must have sudo with NOPASSWD"

    server = RainMoveServerSites()
    server.start()

if __name__ == "__main__":
    main()
#END        
