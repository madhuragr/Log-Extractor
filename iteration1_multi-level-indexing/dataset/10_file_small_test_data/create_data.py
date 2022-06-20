from datetime import datetime
import os

filenames = []
no_of_files = 10

if not os.path.exists('data'):
    os.makedirs('data')

os.chdir('data')
s = "Some Field, Other Field, And so on, Till new line,..."

for j in range (1, no_of_files + 1):
	with open('%d.log' % j, 'w') as f:
		for x in range(1, 11):
			timestr = datetime.now()
			time = str(timestr)
			f.write(time + ", " + s)
			f.write("\n")
	f.close()
