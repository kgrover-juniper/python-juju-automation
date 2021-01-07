import os
import sys
import argparse
import time
import subprocess
from datetime import datetime
minutes = 150


class Deploy(object):
    def __init__ (self, ubuntu, openstack, contrail):
        self.ubuntu = ubuntu
        self.openstack = openstack
        self.contrail = contrail

    def juju_deployment(self):
        global start,end,message,os
        os="18.04" if self.ubuntu=="bionic" else os="20.04"
        start = datetime.now()
        deploy_script = subprocess.call(["./deploy-contrail.sh", self.ubuntu, self.openstack, self.contrail], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return_code, return_message = self.verify_deployment()
        end = datetime.now()
        if return_code == -1:
            message = return_message + "Deployment failed"
        else:
            message = return_message + "Deployement successful"
        message += self.verify_os()

    def verify_deployment(self):
        tries = 0
        status_verified = False
        while (status_verified is False and tries<=minutes):
            tries += 1
            time.sleep(60)
            c1 = subprocess.Popen(["/snap/bin/juju", "status"], stdout=subprocess.PIPE)
            c2 = subprocess.Popen(["grep", "-e allocating", "-e blocked", "-e pending", "-e waiting", "-e maintenance", "-e executing", "-e error"], 
                    stdin=c1.stdout,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout = c2.communicate()[0]
            if not stdout:
                status_verified = True
            c1.wait()
        if status_verified is False:
            return -1,"Tries Expired, "
        else:
            return 0,""
    
    def verify_os(self):
        c1 = subprocess.Popen(["/snap/bin/juju", "show-unit", "ubuntu/0"],stdout=subprocess.PIPE)
        c2 = subprocess.Popen(["grep", "version"],stdin=c1.stdout,stdout=subprocess.PIPE)
        version = c2.communicate()[0]
        if os not in version:
            return ", os-version ERROR"
        else:
            return ", os-version verified"

    def write_result(self):
        result = "\nJuju deployment " + str(self.ubuntu) + " " + str(self.openstack) + " " + str(self.contrail) +  "\n" + message
        result += "\nStarted at " + str(start) + "\nEnded at " + str(end) + "\nTime taken = " + str(end-start) + "\n"
        fout = "result.txt"
        if os.path.exists(fout):
            os.remove(fout)
        with open(fout, 'w') as outfile:
            outfile.write(result)

def parse_cli(args):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-u', '--ubuntu', default='bionic', help='Ubuntu version to deploy (bionic/focal)')
    parser.add_argument('-o', '--openstack', default='ussuri', help='Openstack version to deploy (queens/train/ussuri)')
    parser.add_argument('-c', '--contrail', default='2008.123', help='Contrail version to deploy)')
    pargs = parser.parse_args(args)
    return pargs

def main(ubuntu, openstack, contrail):
    obj = Deploy(ubuntu, openstack, contrail)
    obj.juju_deployment()
    obj.write_result()

if __name__ == "__main__":
    pargs = parse_cli(sys.argv[1:])
    main(pargs.ubuntu, pargs.openstack, pargs.contrail)
