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

def find_no_of_lines(f, start_file_index_padded):
	global size
	# with open('data/LogFile-000001.log', 'rb') as f:
	first_line = (f.readline().decode())
	# print (first_line)
	f.seek(0)
	with open('tmp', 'w+') as f1:
		f1.write(first_line)
	f1.close()
	# f.close()
	size = os.path.getsize('tmp')
	os.remove('tmp')
	file_size = os.stat('data/LogFile-%s.log' % start_file_index_padded).st_size
	no_of_lines = math.ceil(file_size/(size))
	return no_of_lines

def binary_search_function(f, start, end, start_timestamp):
	# start_file_index_padded = str(start_file_index).zfill(6)
	# f = open('data/LogFile-%s.log' % start_file_index_padded, 'rb')
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
	# for line in f:
	# 	print (line)
	# 	break
	start_row_index = binary_search_function(f, 1, no_of_lines, start_timestamp)
	return start_row_index

print (binary_search_to_find_start_timestamp_row(1,1594832976.636915))

