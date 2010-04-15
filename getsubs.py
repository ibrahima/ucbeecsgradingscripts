#!/usr/bin/env python

import subprocess
import os
import re
from optparse import OptionParser

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
	logsregex = "(ok|problem)-" + subsregex
	subsre = re.compile(subsregex)
	logsre = re.compile(logsregex)
	submissions = filter(lambda x: subsre.match(x), f)
	logs = [(logsre.match(x),x) for x in f]
	logs = filter(lambda x: x[0], logs)

	for file in submissions:
		look = subprocess.Popen(["lookat", "-d", file +".d", file])
		look.wait()
		os.remove(file)
	scores = {}
	for log in logs:
		score = getAutograderResult(log[1])
		username = log[0].groups()[1]
		if not username in scores or score > scores[username]:
			scores[username] = score
	users = scores.keys()
	users.sort()
	for user in users:
		print user, " got ", scores[user], "from the autograder"
	os.chdir("..")
	print "Creating %s.tar.bz2" % assign
	tar = subprocess.Popen(["gtar", "cjf", assign+".tar.bz2", "--dereference", assign])
	tar.wait()
	
	
def getAutograderResult(logfile):
	scoreregex = "^Score: (\d{1,2})/(\d{1,2})$"
	cmp = re.compile(scoreregex)
	file = open(logfile)
	score = 0
	for line in file:
		if line.startswith("Score: "):
			m = cmp.match(line)
			if m:
				score = m.groups()[0]
	return score 

def makeRoster(assign):
    out = open(assign+"roster.txt", 'w')
    makeroster = subprocess.Popen(["make-roster", assign], stdout=out)
    makeroster.wait()
    
	
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-m", "--make-roster", action="store_true" ,dest="make_roster")
    (options, args) = parser.parse_args()
    if options.make_roster:
        makeRoster(args[0])
    else:
        getsubs(args[0])