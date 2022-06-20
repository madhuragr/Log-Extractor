
from datetime import datetime

with open("data/1.log", 'rb') as f:
	# first = next(fh).decode()
	num_chars = len(f.readline())
	f.seek(-num_chars, 2)
	# last = f.readlines().decode()
	# last = f.readlines()[-1].decode()
	# last = fh.readline()
	# print (last)
	for i,line in enumerate(f):
		new_line = line.decode()
		date_time = new_line[0:26]
		print (date_time)
		date_time_obj = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S.%f")
		timestamp = datetime.timestamp(date_time_obj)
		print (timestamp)