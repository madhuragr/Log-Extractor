from datetime import datetime
import sys
import os
import numpy as np
import bisect
import threading
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from sortedcontainers import SortedDict
import glob
import time
import pkg_resources.py2_warn
import subprocess

start = time.time()

# LogExtractor.exe -f "From Time" -t "To Time" -i "Log file directory location"

start_time = sys.argv[2]
end_time = sys.argv[4]
# bucket_to_mount = sys.argv[6]

os.system('mkdir -p mount_dir')
subprocess.run(["s3fs", sys.argv[6], "mount_dir", "-o", "passwd_file=passwd_s3fs", "-o", "nonempty"])
# subprocess.run(["s3fs", "testmcqdb", "mount_dir", "-o", "passwd_file=passwd_s3fs", "-o", "nonempty"])

data_location = "mount_dir/data/"

start_date_time_obj = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S.%f")
start_timestamp = datetime.timestamp(start_date_time_obj)
end_date_time_obj = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S.%f')
end_timestamp = datetime.timestamp(end_date_time_obj)

def print_queries_middle_files(file):
	f = open(file, 'r')
	for line in f:
		print (line)
	f.close();

def print_queries_from_start_file(file, start_row_for_linear_search, start_timestamp):
	with open(file, "r") as f:
		num_chars = len(f.readline())
		f.seek(num_chars *(start_row_for_linear_search - 1))
		for i,line in enumerate(f):
			date_time = line[0:26]
			date_time_obj = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S.%f")
			timestamp = datetime.timestamp(date_time_obj)
			if (timestamp >= start_timestamp):
				print (line)
				for i,line in enumerate(f):
					print(line)
	f.close()

def print_queries_from_end_file(file, end_timestamp):
	with open(file, "r") as f:
		for i,line in enumerate(f):
			date_time = line[0:26]
			date_time_obj = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S.%f")
			timestamp = datetime.timestamp(date_time_obj)
			if (timestamp > end_timestamp):
				break
			else:
				print (line)
	f.close()

def print_queries_start_file_same_as_end_file(file, start_row_for_linear_search, start_timestamp, end_timestamp):
	with open(file, "r") as f:
		num_chars = len(f.readline())
		f.seek(num_chars *(start_row_for_linear_search - 1))
		for i,line in enumerate(f):
			date_time = line[0:26]
			date_time_obj = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S.%f")
			timestamp = datetime.timestamp(date_time_obj)
			if (timestamp >= start_timestamp and timestamp <= end_timestamp):
				print (line)
			elif (timestamp > end_timestamp):
				break
	f.close()

timestamp_array = []
filenames = []
filepaths = []
filepaths_ts_array = []

def create_data_structures():
	for files in os.walk(data_location):
		global no_of_files
		no_of_files = len(glob.glob1(data_location,"*.log"))
		for j in range(1, no_of_files + 1):
			filenames.append("%d.log" % j)
			filepaths.append("%d.log" % j)
			filepaths_ts_array.append("%d.log" % j)
		
		# print ("filenames is ", filenames)
		# print ("filepaths is ", filepaths)

		for i in range (0, no_of_files):
			filepaths[i] = {}
			filepaths_ts_array[i] = []

def read_data_to_create_2_level_indices():
		os.chdir(data_location)
		for j in range(1, no_of_files + 1):
			with open('%d.log' % j, 'r') as f:
				for i,line in enumerate(f):
					date_time = line[0:26]
					date_time_obj = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S.%f")
					timestamp = datetime.timestamp(date_time_obj)
					if i == 0:
						timestamp_array.append(timestamp)
						# assumed here that size of each index block is 20
					if (i % 20 == 0):
						filepaths[j-1][timestamp] = i + 1
						filepaths_ts_array[j-1].append(timestamp)
					i = i + 1
			f.close()

create_data_structures()
read_data_to_create_2_level_indices()

# print (filepaths[0])

def binary_search_to_get_positions():
	# Binary search on timestamp on index file to find which file to get into for start_time
	# bisect right returns index (in 1-based index system)
	global start_file_index, end_file_index, start_file, end_file, start_row_for_linear_search

	start_file_index = bisect.bisect_right(timestamp_array, start_timestamp) - 1
	end_file_index = bisect.bisect_right(timestamp_array, end_timestamp) - 1

	start_file = filenames[start_file_index]
	end_file = filenames[end_file_index]

	sd = SortedDict(filepaths[start_file_index])
	# bisect on sorted dict gives index corresponding to the timestamp, in 1-based index system
	index = sd.bisect_right(start_timestamp) - 1
	start_row_for_linear_search = filepaths[start_file_index][filepaths_ts_array[start_file_index][index]]

binary_search_to_get_positions()

# print (start_file_index)
# print (end_file_index)
# print (start_file)
# print (end_file)
# print (start_row_for_linear_search)

def main():
	if (start_file_index > end_file_index):
		sys.exit("Wrong Query Format\n")

	elif(start_file_index == end_file_index):
		print_queries_start_file_same_as_end_file(start_file, start_row_for_linear_search, start_timestamp, end_timestamp)

	elif(end_file_index - start_file_index == 1):
		t1 = threading.Thread(target=print_queries_from_start_file, args=(start_file, start_row_for_linear_search, start_timestamp)) 
		t2 = threading.Thread(target=print_queries_from_end_file, args=(end_file, end_timestamp)) 
		t1.start()
		t2.start()
		t1.join()
		t2.join()	
			
	else:
		t1 = threading.Thread(target=print_queries_from_start_file, args=(start_file, start_row_for_linear_search, start_timestamp)) 
		t2 = threading.Thread(target=print_queries_from_end_file, args=(end_file, end_timestamp)) 
		t1.start()
		t2.start()
		t1.join()
		t2.join()	

		new_file_array = []
		for i in range (start_file_index+1, end_file_index):
			new_file_array.append(filenames[i])
		with ThreadPoolExecutor(max_workers = len(new_file_array)) as executor:
			executor.map(print_queries_middle_files, new_file_array)

main()

end = time.time()
# total time taken
print(f"Runtime of the program is {end - start}")