

def print_queries_from_start_file(start_file_index, start_row_index):
	start_file_index_padded = str(start_file_index).zfill(6)
	with open('data/LogFile-%s.log' % start_file_index_padded, 'rb') as f:
		num_chars = len(f.readline())
		f.seek(num_chars *(start_row_index - 1))
		for i,line in enumerate(f):
			print (line.decode().rstrip())
	f.close()

print_queries_from_start_file(10, 1)