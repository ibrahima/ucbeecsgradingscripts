import subprocess
import os

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



def makeroster(filename, d, outfile):
    f = open(filename)
    r = open(outfile, "w")
    for line in f.readlines():
        r.write("{0} {1} 2\n".format(line.strip(), d[line.strip()].strip()))
    r.close()
    f.close()

if __name__ == "__main__":
	import sys
	getsubs(sys.argv[1])
