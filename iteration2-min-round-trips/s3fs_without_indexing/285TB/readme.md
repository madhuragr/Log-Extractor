Pre-requisites: SSHFS needs to be installed to mount the network file system locally.

Sample command to output query lines : dist/bs_new/bs_new -f "2020-07-15 22:39:36.636863" -t "2020-07-15 22:39:37.275490" -i  "ubuntu@ec2-3-7-253-124.ap-south-1.compute.amazonaws.com:data"

Password to mount the sample data: savethecat

The above command will first create a directory named "mount_dir". Data present on NFS will be mounted on this directory. Query logs present on the NFS data in the requested time range will then be outputted on the machine.

