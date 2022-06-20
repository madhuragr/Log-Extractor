from datetime import datetime
import os
import math

def find_no_of_lines():
	global size
	with open('data/1.log', 'rb') as f:
		first_line = (f.readline().decode())
		# print (first_line.rstrip())
		with open('tmp', 'w+') as f1:
			f1.write(first_line)
		f1.close()
	f.close()
	size = os.path.getsize('tmp')
	os.remove('tmp')
	# size_whole_file = os.path.getsize('data/1.log')
	# 16 gb = 17179860387 bytes 
	# no_of_lines = math.ceil((17179860387)/(size))
	no_of_lines = math.ceil((820)/(size))
	# print (no_of_lines)
	# no_of_lines = math.ceil((83968)/(size))
	return no_of_lines

def binary_search_function(start_file_index, start, end, start_timestamp):
	# open file in binary mode and then use fseek(), this will seek in O(1)
	f = open('data/%d.log' % start_file_index, 'rb')
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
		return binary_search_function(start_file_index, i+1, end, start_timestamp)
	elif (start_timestamp < timestamp):
		return binary_search_function(start_file_index, start, i-1, start_timestamp)
	f.close()

def binary_search_to_find_start_timestamp_row(start_file_index, start_timestamp):
	no_of_lines = find_no_of_lines()
	start_row_index = binary_search_function(start_file_index, 1, no_of_lines, start_timestamp)
	return start_row_index

print (binary_search_to_find_start_timestamp_row(10, 1594589079.944104))

