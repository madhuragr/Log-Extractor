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

start = time.time()

# LogExtractor.exe -f "From Time" -t "To Time" -i "Log file directory location"

start_time = sys.argv[2]
end_time = sys.argv[4]

os.system('mkdir -p mount_dir_ec2')
# os.system("mount -t ubuntu@ec2-3-7-253-124.ap-south-1.compute.amazonaws.com:data/ mount_dir_ec2/")
# subprocess.Popen(["sudo", "mount", "-t", "ubuntu@ec2-3-7-253-124.ap-south-1.compute.amazonaws.com:data/", "mount_dir_ec2/"])
# subprocess.run(["s3fs", sys.argv[6], "mount_dir", "-o", "passwd_file=passwd_s3fs", "-o", "nonempty"])
subprocess.run(["sshfs", sys.argv[6], "mount_dir_ec2/"])

# test argv[6] : aws_ec2:data/
data_location = "mount_dir_ec2/data/"
# data_location = "data"

start_date_time_obj = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S.%f")
start_timestamp = datetime.timestamp(start_date_time_obj)
end_date_time_obj = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S.%f')
end_timestamp = datetime.timestamp(end_date_time_obj)

os.chdir(data_location)

def print_queries_middle_files(file):
	f = open(file, 'rb')
	for line in f:
		print (line.decode().rstrip())
	f.close();

def print_queries_from_start_file(start_file_index, start_row_index):
	start_file_index_padded = str(start_file_index).zfill(6)
	with open('LogFile-%s.log' % start_file_index_padded, 'rb') as f:
		num_chars = len(f.readline())
		f.seek(num_chars *(start_row_index - 1))
		for i,line in enumerate(f):
			print (line.decode().rstrip())
	f.close()

def print_queries_from_end_file(end_file_index, end_timestamp):
	end_file_index_padded = str(end_file_index).zfill(6)
	with open('LogFile-%s.log' % end_file_index_padded, 'rb') as f:
		for i,line in enumerate(f):
			date_time = line[0:26]
			date_time_obj = datetime.strptime(date_time.decode(), "%Y-%m-%d %H:%M:%S.%f")
			timestamp = datetime.timestamp(date_time_obj)
			if (timestamp > end_timestamp):
				break
			else:
				print (line.decode().rstrip())
	f.close()

def print_queries_start_file_same_as_end_file(file_index, start_row_index, end_timestamp):
	file_index_padded = str(file_index).zfill(6)
	with open('LogFile-%s.log' % file_index_padded, 'rb') as f:
		num_chars = len(f.readline())
		f.seek(num_chars *(start_row_index - 1))
		for i,line in enumerate(f):
			date_time = line[0:26]
			date_time_obj = datetime.strptime(date_time.decode(), "%Y-%m-%d %H:%M:%S.%f")
			timestamp = datetime.timestamp(date_time_obj)
			if (timestamp <= end_timestamp):
				print (line.decode().rstrip())
			elif (timestamp > end_timestamp):
				break
	f.close()

def binary_search_to_find_start_file(start, end, start_timestamp):
	if(start == end):
		return start
	elif (end - start == 1):
		start_padded = str(start).zfill(6)
		with open('LogFile-%s.log' % start_padded, 'rb') as f:
			num_chars = len(f.readline())
			f.seek(-num_chars, 2)
			for i,line in enumerate(f):
				date_time = line[0:26]
				date_time_obj = datetime.strptime(date_time.decode(), "%Y-%m-%d %H:%M:%S.%f")
				last_timestamp_in_start_file = datetime.timestamp(date_time_obj)
				# break # no need to break .. already at last line
		f.close()
		
		if(start_timestamp > last_timestamp_in_start_file):
			return end
		else:
			return start

	i = (start+end)//2
	i_padded = str(i).zfill(6)
	with open('LogFile-%s.log' % i_padded, 'rb') as f:
		for j,line in enumerate(f):
			date_time = line[0:26]
			date_time_obj = datetime.strptime(date_time.decode(), "%Y-%m-%d %H:%M:%S.%f")
			timestamp = datetime.timestamp(date_time_obj)
			break
		if (start_timestamp == timestamp):
			return i
		elif (start_timestamp > timestamp):
			return binary_search_to_find_start_file(i, end, start_timestamp)
		elif (start_timestamp < timestamp):
			return binary_search_to_find_start_file(start, i, start_timestamp)

def binary_search_to_find_end_file(start, end, end_timestamp):
	if(start == end):
		return start
	elif (end - start == 1):
		end_padded = str(end).zfill(6)
		with open('LogFile-%s.log' % end_padded, 'rb') as f:
			for j,line in enumerate(f):
				date_time = line[0:26]
				date_time_obj = datetime.strptime(date_time.decode(), "%Y-%m-%d %H:%M:%S.%f")
				first_timestamp_in_end_file = datetime.timestamp(date_time_obj)
				break
		f.close()

		if(end_timestamp < first_timestamp_in_end_file):
			return start
		else:
			return end

	i = (start+end)//2
	i_padded = str(i).zfill(6)
	with open('LogFile-%s.log' % i_padded, 'rb') as f:
		for j,line in enumerate(f):
			date_time = line[0:26]
			date_time_obj = datetime.strptime(date_time.decode(), "%Y-%m-%d %H:%M:%S.%f")
			timestamp = datetime.timestamp(date_time_obj)
			break
		if (end_timestamp == timestamp):
			return i
		elif (end_timestamp > timestamp):
			return binary_search_to_find_end_file(i, end, end_timestamp)
		elif (end_timestamp < timestamp):
			return binary_search_to_find_end_file(start, i-1, end_timestamp)

def find_no_of_lines(f, start_file_index_padded):
	global size
	first_line = (f.readline().decode())
	f.seek(0)
	with open('tmp', 'w+') as f1:
		f1.write(first_line)
	f1.close()
	size = os.path.getsize('tmp')
	os.remove('tmp')
	file_size = os.stat('LogFile-%s.log' % start_file_index_padded).st_size
	no_of_lines = math.ceil(file_size/(size))
	return no_of_lines

def binary_search_function(f, start, end, start_timestamp):
	# open file in binary mode and then use fseek(), this will seek in O(1)
	if(start > end):
		return start
	
	i = (start+end)//2
	num_chars = len(f.readline())
	# By chance if the last log line in the file is not followed by new line character
	if(num_chars != size):
		num_chars = num_chars + 1
	
	f.seek(num_chars *(i - 1))
	for j,line in enumerate(f):
		date_time = line[0:26]
		date_time_obj = datetime.strptime(date_time.decode(), "%Y-%m-%d %H:%M:%S.%f")
		timestamp = datetime.timestamp(date_time_obj)
		break
	if (start_timestamp == timestamp):
		return i
	if (start_timestamp > timestamp):
		return binary_search_function(f, i+1, end, start_timestamp)
	elif (start_timestamp < timestamp):
		return binary_search_function(f, start, i-1, start_timestamp)
	f.close()

def binary_search_to_find_start_timestamp_row(start_file_index, start_timestamp):
	start_file_index_padded = str(start_file_index).zfill(6)
	f = open('data/LogFile-%s.log' % start_file_index_padded, 'rb')
	no_of_lines = find_no_of_lines(f, start_file_index_padded)
	start_row_index = binary_search_function(f, 1, no_of_lines, start_timestamp)
	return start_row_index

def main():

	start_file_index = binary_search_to_find_start_file(1, 200, start_timestamp)
	end_file_index = binary_search_to_find_end_file(1, 200, end_timestamp)
	start_row_index = binary_search_to_find_start_timestamp_row(start_file_index, start_timestamp)
	
	if(start_timestamp > end_timestamp):
		sys.exit("Wrong Query Format\n")

	elif(start_file_index == end_file_index):
		print_queries_start_file_same_as_end_file(start_file_index, start_row_index, end_timestamp)

	elif(end_file_index - start_file_index == 1):
		t1 = threading.Thread(target=print_queries_from_start_file, args=(start_file_index, start_row_index)) 
		t2 = threading.Thread(target=print_queries_from_end_file, args=(end_file_index, end_timestamp)) 
		t1.start()
		t2.start()
		t1.join()
		t2.join()	
			
	else:
		t1 = threading.Thread(target=print_queries_from_start_file, args=(start_file_index, start_row_index)) 
		t2 = threading.Thread(target=print_queries_from_end_file, args=(end_file_index, end_timestamp)) 
		t1.start()
		t2.start()
		t1.join()
		t2.join()	
		new_file_array = []
		for i in range (start_file_index+1, end_file_index):
			i_padded = str(i).zfill(6)
			new_file_array.append('LogFile-%s.log' % i_padded)
		with ThreadPoolExecutor(max_workers = len(new_file_array)) as executor:
			executor.map(print_queries_middle_files, new_file_array)
		
main()

end = time.time()
# total time taken
print(f"Runtime of the program is {end - start}")

# subprocess.run(["fusermount", "-u", "mount_dir_ec2"])
