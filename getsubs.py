import subprocess
import os
import re

def makedict(filename):
	f = open(filename)
	d={}
	for line in f.readlines():
		parseline(line, d)
	return d

def parseline(line, d):
	(uid, name) = line.split()
	d[uid]=name

def getsubs(assign, rosterfile="roster"):
	if not os.path.isfile(rosterfile):
		makeroster("mysortedroster.txt", makedict("sorted.txt"), rosterfile)
	d = makedict("sorted.txt")	
	if not os.path.exists(assign):
		os.mkdir(assign)
	f = open("mysortedroster.txt")
	r = open("%sroster"%assign, "w")

	for uid in [x.strip() for x in f.readlines()]:
		os.mkdir(assign + "/" + uid[-2:])
		os.chdir(assign + "/" + uid[-2:])
		proc = subprocess.Popen(["get-subm", assign, uid], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		output, err = proc.communicate()
		if err[:10] == "No entries":
			r.write("{0} {1} 0 No submission\n".format(uid, d[uid]))
		else:
			r.write("{0} {1} 2\n".format(uid, d[uid]))
		os.chdir("../..")
	r.close()
	f.close()

def getsubs2(assign):
	if not os.path.exists(assign):
		os.mkdir(assign)
	os.chdir(assign)
	proc = subprocess.Popen(["get-submissions", assign])
	proc.wait()
	gen = os.walk(".")
	r, d, f = gen.next()
	regex = "cs61c-[a-z][a-z].\d{12,12}"
	p = re.compile(regex)
	filtered = filter(lambda x: p.match(x), f) #only unpack assignments, not autograder results
	for file in filtered:
		print "Looking at ", file
		look = subprocess.Popen(["lookat", file, "-d " +file +".d"])
		look.wait()
		os.remove(file)

def makeroster(filename, d, outfile):
    f = open(filename)
    r = open(outfile, "w")
    for line in f.readlines():
        r.write("{0} {1} 2\n".format(line.strip(), d[line.strip()].strip()))
    r.close()
    f.close()

if __name__ == "__main__":
	import sys
	getsubs2(sys.argv[1])
