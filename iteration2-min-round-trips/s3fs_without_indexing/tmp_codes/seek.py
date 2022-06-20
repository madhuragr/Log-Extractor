import os

# f = open('data/1.log', 'r')
# # i = (start+end)//2
# i = 1
# num_chars = len(f.readline()) # check if -1 is req for new line character

# for line in f:
# 	print (line.rstrip())
# 	break

# f.seek(num_chars *(i - 1))
# # print (f.readline())
# # print (f.readline())
# # for line in f:
# # 	print (line.rstrip())
# # 	break

os.chdir('data')

start_file_index = 1
start_row_index = 5
def print_queries_from_start_file(start_file_index, start_row_index):
	# with open('%d.log' % start_file_index, 'rb') as f:
	with open('%d.log' % start_file_index, 'r') as f:
		num_chars = len(f.readline())
		f.seek(num_chars *(start_row_index - 1))
		for i,line in enumerate(f):
			print (line)
	f.close()

print_queries_from_start_file(start_file_index, start_row_index)

