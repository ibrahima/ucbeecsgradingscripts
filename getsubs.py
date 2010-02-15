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
	subsre = re.compile(subsregex)
	logsre = re.compile(logsregex)
	submissions = filter(lambda x: subsre.match(x), f)
	logs = filter(lambda x: logsre.match(x), f)
	for file in submissions:
		look = subprocess.Popen(["lookat", "-d", file +".d", file])
		look.wait()
		os.remove(file)
	os.chdir("..")
	tar = subprocess.Popen(["gtar", "cjvf", assign+"tar.bz2", "--dereference", assign])
	tar.wait()
	
if __name__ == "__main__":
	import sys
	getsubs(sys.argv[1])
