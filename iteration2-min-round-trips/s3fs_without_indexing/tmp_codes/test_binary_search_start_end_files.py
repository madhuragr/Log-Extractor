from datetime import datetime
import sys
import os

os.chdir("data")

# def binary_search_to_find_start_file(start, end, start_timestamp):
# 	if(start == end):
# 		return start
# 	elif (end - start == 1):
# 		# with open('%d.log' % end, 'r') as f:
# 		# 	for j,line in enumerate(f):
# 		# 		date_time = line[0:26]
# 		# 		date_time_obj = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S.%f")
# 		# 		first_timestamp_in_end_file = datetime.timestamp(date_time_obj)
# 		# 		break
# 		# f.close()
# 		with open('%d.log' % start, 'rb') as f:
# 			num_chars = len(f.readline())
# 			f.seek(-num_chars, 2)
# 			for i,line in enumerate(f):
# 				new_line = line.decode()
# 				date_time = new_line[0:26]
# 				date_time_obj = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S.%f")
# 				last_timestamp_in_start_file = datetime.timestamp(date_time_obj)
# 		f.close()
		
# 		# if((start_timestamp >= first_timestamp_in_end_file) or (start_timestamp > last_timestamp_in_start_file)):
# 		if(start_timestamp > last_timestamp_in_start_file):
# 			return end
# 		else:
# 			return start

# 	i = (start+end)//2
# 	with open('%d.log' % i, 'r') as f:
# 		for j,line in enumerate(f):
# 			date_time = line[0:26]
# 			date_time_obj = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S.%f")
# 			timestamp = datetime.timestamp(date_time_obj)
# 			break
# 		if (start_timestamp == timestamp):
# 			return i
# 		elif (start_timestamp > timestamp):
# 			return binary_search_to_find_start_file(i, end, start_timestamp)
# 		elif (start_timestamp < timestamp):
# 			return binary_search_to_find_start_file(start, i-1, start_timestamp)

# file_number5_5 = binary_search_to_find_start_file(1, 10, 1594589079.943529)
# file_number1_1 = binary_search_to_find_start_file(1, 10, 1594589079.942978)
# file_number5_1 = binary_search_to_find_start_file(1, 10, 1594589079.943009)
# file_number1_2 = binary_search_to_find_start_file(1, 10, 1594589079.943113)
# # file_number1_2 = binary_search_to_find_start_file(1, 10, 1594589079.943560)
# file_number1_10 = binary_search_to_find_start_file(1, 10, 1594589079.944071)
# file_number5_10 = binary_search_to_find_start_file(1, 10, 1594589079.944085)
# file_number10_10 = binary_search_to_find_start_file(1, 10, 1594589079.9441)
# file_number20_10 = binary_search_to_find_start_file(1, 10, 1594589079.9442)
# file_number11_9 = binary_search_to_find_start_file(1, 10, 1594589079.944028)
# file_number10_9 = binary_search_to_find_start_file(1, 10, 1594589079.944027)

# # CASE WHEN TIMESTAMP > LAST OF 9.LOG AND < 10.LOG THEN RIGHT NOW, CODE IS RETURNING 9,
# # ACTUALLY IT SHOULD RETURN 10.LOG
# print (file_number11_9)
# print (file_number10_9)

# print (file_number5_5)
# print (file_number1_1)
# print (file_number5_1)
# print (file_number1_2)
# print (file_number1_10)
# print (file_number5_10)
# print (file_number10_10)
# print (file_number11_10)

# line 5 of 5.log : 1594589079.943529 
# line 1 of 1.log : 1594589079.942978 
# line 5 of 1.log : 1594589079.943009
# line 1 of 2.log : 1594589079.943113 
# line 1 of 10.log : 1594589079.944071
# line 5 of 10.log : 1594589079.944085
# line 10 of 10.log : 1594589079.9441
# line 11 of 10.log (hypothetical) : 1594589079.9442
# line 11 of 10.log (hypothetical) : 1594589079.9442
# line 10 of 9.log : 1594589079.944027
# line 11 of 9.log (hypothetical) : 1594589079.944028


def binary_search_to_find_end_file(start, end, end_timestamp):
	if(start == end):
		return start
	elif (end - start == 1):
		with open('%d.log' % end, 'r') as f:
			for j,line in enumerate(f):
				date_time = line[0:26]
				date_time_obj = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S.%f")
				first_timestamp_in_end_file = datetime.timestamp(date_time_obj)
				break
		f.close()

		if(end_timestamp < first_timestamp_in_end_file):
			return start
		else:
			return end

	i = (start+end)//2
	with open('%d.log' % i, 'r') as f:
		for j,line in enumerate(f):
			date_time = line[0:26]
			date_time_obj = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S.%f")
			timestamp = datetime.timestamp(date_time_obj)
			break
		if (end_timestamp == timestamp):
			return i
		elif (end_timestamp > timestamp):
			return binary_search_to_find_end_file(i, end, end_timestamp)
		elif (end_timestamp < timestamp):
			return binary_search_to_find_end_file(start, i-1, end_timestamp)

# file_number5_5 = binary_search_to_find_end_file(1, 10, 1594589079.943529)
# file_number1_1 = binary_search_to_find_end_file(1, 10, 1594589079.942978)
# file_number5_1 = binary_search_to_find_end_file(1, 10, 1594589079.943009)
# file_number1_2 = binary_search_to_find_end_file(1, 10, 1594589079.943113)
# file_number1_2 = binary_search_to_find_end_file(1, 10, 1594589079.943560)
file_number1_10 = binary_search_to_find_end_file(1, 10, 1594589079.944071)
file_number5_10 = binary_search_to_find_end_file(1, 10, 1594589079.944085)
file_number5_1 = binary_search_to_find_end_file(1, 10, 1594589079.943009)
file_number1_2 = binary_search_to_find_end_file(1, 10, 1594589079.943113)
file_number10_10 = binary_search_to_find_end_file(1, 10, 1594589079.9441)
file_number11_10 = binary_search_to_find_end_file(1, 10, 1594589079.9442)
file_number11_9 = binary_search_to_find_end_file(1, 10, 1594589079.944028)
file_number10_9 = binary_search_to_find_end_file(1, 10, 1594589079.944027)

# CASE WHEN TIMESTAMP > LAST OF 9.LOG AND < 10.LOG THEN RIGHT NOW, CODE IS RETURNING 9,
# ACTUALLY IT SHOULD RETURN 10.LOG
print (file_number11_9)
print (file_number10_9)

# print (file_number5_5)
# print (file_number1_1)
# print (file_number5_1)
# print (file_number1_2)
# print (file_number1_10)
# print (file_number5_1)
# print (file_number1_2)
# print (file_number5_10)
# print (file_number10_10)
# print (file_number11_10)

# line 5 of 5.log : 1594589079.943529 
# line 1 of 1.log : 1594589079.942978 
# line 5 of 1.log : 1594589079.943009
# line 1 of 2.log : 1594589079.943113 
# line 1 of 10.log : 1594589079.944071
# line 5 of 10.log : 1594589079.944085
# line 10 of 10.log : 1594589079.9441
# line 11 of 10.log (hypothetical) : 1594589079.9442
# line 10 of 9.log : 1594589079.944027
# line 11 of 9.log (hypothetical) : 1594589079.944028

