from datetime import datetime
import os

filenames = []
no_of_files = 200

if not os.path.exists('data'):
    os.makedirs('data')

os.chdir('data')
s = "Some Field, Other Field, And so on, Till new line,..."

for j in range (1, no_of_files + 1):
	j_padded = str(j).zfill(6)
	with open('LogFile-%s.log' % j_padded, 'w') as f:
		for x in range(1, 1001):
			timestr = datetime.now()
			time = str(timestr)
			f.write(time + ", " + s)
			f.write("\n")
	f.close()
