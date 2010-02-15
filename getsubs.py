import subprocess
import os
import re

def getsubs(assign):
	if not os.path.exists(assign):
		os.mkdir(assign)
	os.chdir(assign)
	proc = subprocess.Popen(["get-submissions", assign])
	proc.wait()
	gen = os.walk(".")
	r, d, f = gen.next()
	f.sort()
	subsregex = "(cs61c-[a-z][a-z]).\d{12,12}"
	logsregex = "[ok|problem]-" + subsregex
	p = re.compile(subsregex)
	for file in f:
		if p.match(file):#only try to unpack valid submissions, not log files
			look = subprocess.Popen(["lookat", "-d", file +".d", file])
			look.wait()
		os.remove(file)

if __name__ == "__main__":
	import sys
	getsubs(sys.argv[1])
