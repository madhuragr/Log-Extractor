from datetime import datetime
import sys
import os
import threading
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import time
import pkg_resources.py2_warn
import subprocess
import math

# LogExtractor.exe -f "From Time" -t "To Time" -i "Log file directory location"

start = time.time()
start_time = sys.argv[2]
end_time = sys.argv[4]
os.system('mkdir -p mount_dir')
subprocess.run(["sshfs", sys.argv[6], "mount_dir/"])

# test argv[6] : aws_ec2:data/
data_location = "mount_dir"
# data_location = "data"

start_date_time_obj = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S.%f")
start_timestamp = datetime.timestamp(start_date_time_obj)
end_date_time_obj = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S.%f')
end_timestamp = datetime.timestamp(end_date_time_obj)
i_pointer = -1

os.chdir(data_location)

if(start_timestamp > end_timestamp):
	sys.exit("Wrong Query Format")

def print_rows_below(f, i, num_chars, i_pointer, end_timestamp):
	for j,line in enumerate(f, i):
		if (j == i_pointer):
			return 
		date_time = line[0:26]
		date_time_obj = datetime.strptime(date_time.decode(), "%Y-%m-%d %H:%M:%S.%f")
		timestamp = datetime.timestamp(date_time_obj)
		if (timestamp <= end_timestamp):
			print (line.decode().rstrip())
		elif (timestamp > end_timestamp):
			return

def print_current_file(f, end_timestamp):
	for i,line in enumerate(f):
		date_time = line[0:26]
		date_time_obj = datetime.strptime(date_time.decode(), "%Y-%m-%d %H:%M:%S.%f")
		timestamp = datetime.timestamp(date_time_obj)
		if (timestamp <= end_timestamp):
			print (line.decode().rstrip())
		elif (timestamp > end_timestamp):
			return

def print_below_files(i, end, end_timestamp):
	if(i > end):
		return
	i_padded = str(i).zfill(6)
	with open('LogFile-%s.log' % i_padded, 'rb') as f:
		for j,line in enumerate(f):
				date_time = line[0:26]
				date_time_obj = datetime.strptime(date_time.decode(), "%Y-%m-%d %H:%M:%S.%f")
				timestamp = datetime.timestamp(date_time_obj)
				if (timestamp <= end_timestamp):
					print (line.decode().rstrip())
				elif (timestamp > end_timestamp):
					f.close()
					return
	f.close()
	print_below_files(i+1, end, end_timestamp)


def find_no_of_lines(f, start_file_index_padded):
	global size
	one_line = (f.readline().decode())
	# f.seek(0)
	with open('tmp', 'w+') as f1:
		f1.write(one_line)
	f1.close()
	size = os.path.getsize('tmp')
	os.remove('tmp')
	file_size = os.stat('LogFile-%s.log' % start_file_index_padded).st_size
	no_of_lines = math.ceil(file_size/(size))
	return no_of_lines


def binary_search_row(f, start, end, i_pointer, start_timestamp, end_timestamp):
	if(start > end):
		return
	i = (start + end)//2
	num_chars = len(f.readline())
	# By chance if the last log line in the file is not followed by new line character
	if(num_chars != size):
		# num_chars = num_chars + 1
		num_chars = size
	
	f.seek(num_chars *(i - 1))
	for j,line in enumerate(f):
		date_time = line[0:26]
		date_time_obj = datetime.strptime(date_time.decode(), "%Y-%m-%d %H:%M:%S.%f")
		timestamp = datetime.timestamp(date_time_obj)
		break
	
	if (start_timestamp == timestamp):
		# file pointer has moved ahead by one line
		f.seek(num_chars *(i - 1))
		print_rows_below(f, i, num_chars, i_pointer, end_timestamp) 
	
	elif (start_timestamp > timestamp):
		binary_search_row(f, i+1, end, i_pointer, start_timestamp, end_timestamp)
	
	elif (end_timestamp < timestamp):
		binary_search_row(f, start, i-1, i_pointer, start_timestamp, end_timestamp)
	
	elif (start_timestamp < timestamp and timestamp <= end_timestamp):
		# file pointer has moved ahead by one line 
		# i_pointer : lines below this line no have already been printed
		f.seek(num_chars *(i - 1))
		print_rows_below(f, i, num_chars, i_pointer, end_timestamp) 
		i_pointer = i
		binary_search_row(f, start, i-1, i_pointer, start_timestamp, end_timestamp)


def binary_search(start, end, start_timestamp, end_timestamp):

	if (start > end):
		return
	if (end - start == 1):

		start_padded = str(start).zfill(6)
		f_start = open('LogFile-%s.log' % start_padded, 'rb')
		num_chars = len(f_start.readline())
		f_start.seek(-num_chars, 2)
		for i,line in enumerate(f_start):
			date_time = line[0:26]
			date_time_obj = datetime.strptime(date_time.decode(), "%Y-%m-%d %H:%M:%S.%f")
			last_timestamp_start_file = datetime.timestamp(date_time_obj)
			# break # no need to break, already at last line

		if(end_timestamp <= last_timestamp_start_file):
			# both start and end queries lie in start file
			# start file pointer is at end of file. Move it 2 lines up
			f_start.seek(-num_chars*2, 2)
			no_of_lines = find_no_of_lines(f_start, start_padded)
			# start file pointer now points to the last line
			binary_search_row(f_start, 1, no_of_lines, i_pointer, start_timestamp, end_timestamp)

		elif (start_timestamp > last_timestamp_start_file):
			# both start and end queries lie in end file
			end_padded = str(end).zfill(6)
			f_end = open('LogFile-%s.log' % end_padded, 'rb')
			no_of_lines = find_no_of_lines(f_end, end_padded)
			binary_search_row(f_end, 1, no_of_lines, i_pointer, start_timestamp, end_timestamp)

		else:
			# start query in start file and end query in end file
			end_padded = str(end).zfill(6)
			f_end = open('LogFile-%s.log' % end_padded, 'rb')
			t1 = threading.Thread(target=print_current_file, args=(f_end, end_timestamp)) 
			t1.start()
			# start file pointer is at end of file. Move it 2 lines up
			f_start.seek(-num_chars*2, 2)
			no_of_lines = find_no_of_lines(f_start, start_padded)
			# start file pointer now points to the last line
			binary_search_row(f_start, 1, no_of_lines, i_pointer, start_timestamp, end_timestamp)			
			t1.join()

	else:
		i = (start+end)//2
		i_padded = str(i).zfill(6)
		with open('LogFile-%s.log' % i_padded, 'rb') as f:
			for j,line in enumerate(f):
				date_time = line[0:26]
				date_time_obj = datetime.strptime(date_time.decode(), "%Y-%m-%d %H:%M:%S.%f")
				timestamp = datetime.timestamp(date_time_obj)
				break
			if (start_timestamp == timestamp):
				f.seek(0) # because one line was traversed while calc timestep above
				t1 = threading.Thread(target=print_current_file, args=(f, end_timestamp)) 
				t2 = threading.Thread(target=print_below_files, args=(i+1, end, end_timestamp)) 
				t1.start()
				t2.start()
				t1.join()
				t2.join()

			elif (start_timestamp > timestamp):
				if(start == end):
					no_of_lines = find_no_of_lines(f, i_padded)
					binary_search_row(f, 1, no_of_lines, i_pointer, start_timestamp, end_timestamp)
				elif(start != end):
					binary_search(i, end, start_timestamp, end_timestamp)

			elif (end_timestamp < timestamp):
				binary_search(start, i-1, start_timestamp, end_timestamp)

			elif (start_timestamp < timestamp and timestamp <= end_timestamp):
				f.seek(0)
				t1 = threading.Thread(target=print_current_file, args=(f, end_timestamp)) 
				t2 = threading.Thread(target=print_below_files, args=(i+1, end, end_timestamp)) 
				t3 = threading.Thread(target=binary_search, args=(start, i-1, start_timestamp, end_timestamp)) 
				t1.start()
				t2.start()
				t3.start()
				t1.join()
				t2.join()
				t3.join()


binary_search(1, 18203, start_timestamp, end_timestamp)
end = time.time()
# print(f"Runtime of the program is {end - start}")
