import paramiko
from shell.Cas5Data import Cas5Data
from shell.Cas3Data import Cas3Data
from shell.applog import Applog
from shell import applog
from shell.Cloudos2Data import Cloudos2Data
from shell.Cloudos3Data import Cloudos3Data
logfile = applog.Applog()

@applog.logRun(logfile)
def casVersionCheck(ip, sshUser, sshPassword):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh.connect(ip, 22, sshUser, sshPassword)
    stdin, stdout, stderr = ssh.exec_command("cat /etc/cas_cvk-version | awk 'NR==1{print $2}'")
    version = stdout.read().decode().strip()
    ssh.close()
    return version

@applog.logRun(logfile)
def cloudosVersionCheck(ip, sshUser, sshPassword):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh.connect(ip, 22, sshUser, sshPassword)
    stdin, stdout, stderr = ssh.exec_command("docker images | grep openstack-com | head -1 | awk '{print $2}'")
    ver = stdout.read().decode().strip()
    version = ver[0]
    version += ver[1]
    ssh.close()
    return version

@applog.logRun(logfile)
def casCollect(ip, sshUser, sshPassword, httpUser, httpPassword):
    logfile = Applog()
    func = {
        'V3.0': Cas3Data,
        'V5.0': Cas5Data
    }
    version = casVersionCheck(ip, sshUser, sshPassword)
    cas = func[version](ip, sshUser, sshPassword, httpUser, httpPassword)
    cas.cvmBasicCollect()
    cas.clusterCollect()
    cas.cvkBasicCollect()
    cas.cvkDiskCollect()
    cas.cvkVswitchCollect()
    cas.cvkStorpoolCollect()
    cas.cvkSharepoolCollect()
    cas.cvkNetsworkCollect()
    cas.vmBasicCollect()
    cas.vmDiskCollect()
    cas.vmNetworkCollect()
    cas.vmDiskRateCollect()
    cas.cvmBackupEnbleCollect()
    cas.cvmHACollect()
    cas.vmBackupPolicyCollect()
    return cas.casInfo

@applog.logRun(logfile)
def cloudosCollect(ip, sshUser, sshPassword, httpUser, httpPassword):
    version = cloudosVersionCheck(ip, sshUser, sshPassword)
    logfile = Applog()
    func = {
        'E1': Cloudos2Data,
        'E3': Cloudos3Data
    }
    cloud = func[version](ip, sshUser, sshPassword, httpUser, httpPassword)
    cloud.NodeCollect()
    cloud.findMaster()
    cloud.diskRateCollect()
    cloud.memRateCollect()
    cloud.cpuRateCollect()
    cloud.containerStateCollect()
    cloud.dockerImageCheck()
    cloud.shareStorErrorCollect()
    cloud.containerServiceCollect()
    cloud.containerLBCollect()
    cloud.imageCollect()
    cloud.vmCollect()
    cloud.vdiskCollect()
    cloud.cloudosBasicCellect()
    cloud.diskCapacity()
    cloud.nodeNtpTimeCollect()
    return cloud.osInfo

# if __name__ == '__main__':
#     # casinfo = casCollect('192.168.2.5', 'root', 'h3c.com!', 'admin', 'admin')
#     # print(casinfo)
#     casinfo2 = casCollect('192.168.2.134', 'root', 'h3c.com!', 'admin', 'admin')
#     print(casinfo2)
#     # os1 = cloudosCollect('192.168.2.189', 'root', 'cloudos', 'admin', 'cloudos')
#     # print(os1)
#     os2 = cloudosCollect('192.168.2.132', 'root', 'cloudos', 'admin', 'h3c.com!')
#     print(os2)

