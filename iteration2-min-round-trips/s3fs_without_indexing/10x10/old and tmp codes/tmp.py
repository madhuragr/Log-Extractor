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

def print_rows_below(f):
	for j,line in enumerate(f):
		print (line)
		break

f= open('data/LogFile-000010.log', 'rb')
# with open('data/LogFile-000010.log', 'rb') as f:
for j,line in enumerate(f, 10):
	print (j, line)
	if (j == 13):
		print ("in")
		print_rows_below(f)
		print ("finished")
		# print (line)
		break

f.seek(0)
for line in enumerate(f):
	print (line)
	break