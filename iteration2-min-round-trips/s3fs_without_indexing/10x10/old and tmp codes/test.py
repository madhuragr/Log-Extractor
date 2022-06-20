import os
import math
def find_no_of_lines(start_file_index):
	global size
	with open('data/LogFile-000001.log', 'rb') as f:
		first_line = (f.readline().decode())
		with open('tmp', 'w+') as f1:
			f1.write(first_line)
		f1.close()
	f.close()
	size = os.path.getsize('tmp')
	os.remove('tmp')
	# 16 gb = 17179860387 bytes 
	# no_of_lines = math.ceil((17179860387)/(size))
	start_file_index_padded = str(start_file_index).zfill(6)
	file_size = os.stat('data/LogFile-%s.log' % start_file_index_padded).st_size
	print (file_size)
	no_of_lines = math.ceil(file_size/(size))
	# no_of_lines = math.ceil((82000)/(size))
	return no_of_lines

print (find_no_of_lines(10))