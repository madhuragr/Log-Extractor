import nfslib

# Context-full access (1-time mount nfs directory)
# nfs = libnfs.NFS('nfs://127.0.0.1/data/tmp/')
nfs = libnfs.NFS('aws_ec2:new/')
# a = nfs.open('/LogFile-000001.log', mode='r')
# a.write("Test string")
# a.close()
print (nfs.open('/LogFile-000001.log', mode='r').read())

