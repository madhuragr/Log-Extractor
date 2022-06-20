import os
import sys
import subprocess
# os.cmd ("mkdir ~/mnt/data_dir mount -t data:/dir/ /mnt/data_dir")

print(sys.argv[1])
# bucket_to_mount = sys.argv[1]
# os.system('s3fs sys.argv[1] mount_dir -o passwd_file=passwd_s3fs -o nonempty')
subprocess.run(["s3fs", sys.argv[1], "mount_dir", "-o", "passwd_file=passwd_s3fs", "-o", "nonempty"])
# subprocess.run(["ls", "-l"])
# os.system('s3fs "sys.argv[1]" mount_dir/ -o passwd_file=passwd_s3fs -o nonempty')
# os.system('wait')
# os.system('cd mount_dir/data')
# os.system('ls')
# os.system('cd ../..')
# os.system('sudo umount -l mount_dir')