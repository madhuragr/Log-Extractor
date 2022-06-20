import os
from datetime import datetime
import math

def find_no_of_lines():
	global no_of_lines, size

	with open('data/1.log', 'r') as f:
		first_line = (f.readline())
		with open('tmp', 'w+') as f1:
			f1.write(first_line)
		f1.close()
	f.close()

	size = os.path.getsize('tmp')
	# print (size)

	# size = 112
	# 16 gb = 17179860387 bytes 
	# no_of_lines = (17179860387)/(size-1)
	no_of_lines = math.ceil((820)/(size))
	# no_of_lines = ((820)/(size))
	# print (no_of_lines)
	# -1 byte for new line character 


f = open('data/1.log', 'r')
# # def binary_search_to_find_start_timestamp_row(file_index, start, end, start_timestamp):
def binary_search_to_find_start_timestamp_row(start, end, start_timestamp):
# 	# open file in binary mode and then use fseek(), this will seek in O(1)
# 	# with open('data/%d.log' % file_index, 'r') as f:
	
# 	# if(start == end):
# 	# 	print ("here")
# 	# 	return start
	
	if(start > end):
		# print ("here")
		return start

	i = (start+end)//2
	# print (start, end, i)

	num_chars = len(f.readline()) # check if -1 is req for new line character
	# By chance if the last log line in the file is not followed by new line character
	if(num_chars != size):
		num_chars = num_chars + 1
	f.seek(num_chars *(i - 1))
	for j,line in enumerate(f):
		date_time = line[0:26]
		date_time_obj = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S.%f")
		timestamp = datetime.timestamp(date_time_obj)
		break
	if (start_timestamp == timestamp):
		return i
	# print (start, end, i, start_timestamp, timestamp)
	if (start_timestamp > timestamp):
		return binary_search_to_find_start_timestamp_row(i+1, end, start_timestamp)
	elif (start_timestamp < timestamp):
		return binary_search_to_find_start_timestamp_row(start, i-1, start_timestamp)

find_no_of_lines()

# # start_timestamp = 
# # binary_search_to_find_start_timestamp_row(1, no_of_lines, start_timestamp)


# file_number1_1 = binary_search_to_find_start_timestamp_row(1, no_of_lines, 1594589079.942978)
# # file_number1_1 = binary_search_to_find_start_timestamp_row(1, no_of_lines, 1594589079.942979)
# # file_number2_1 = binary_search_to_find_start_timestamp_row(1, no_of_lines, 1594589079.942997)
file_number5_1 = binary_search_to_find_start_timestamp_row(1, no_of_lines, 1594589079.943009)
# # # file_number5_1 = binary_search_to_find_start_timestamp_row(1, no_of_lines, 1594589079.943010)
# # file_number7_1 = binary_search_to_find_start_timestamp_row(1, no_of_lines, 1594589079.943015)
# file_number7_1 = binary_search_to_find_start_timestamp_row(1, no_of_lines, 1594589079.943016)
# file_number10_1 = binary_search_to_find_start_timestamp_row(1, no_of_lines, 1594589079.943025)

# print (file_number1_1)
# # print (file_number2_1)
print (file_number5_1)
# print (file_number7_1)
# print (file_number10_1)



