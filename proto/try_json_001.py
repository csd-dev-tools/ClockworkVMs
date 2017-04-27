#!/usr/bin/python

import json

jfp = open("centos.json", "r")
jstuff = json.load(jfp)
print "\n"
for key, value in jstuff.iteritems():
    print str(key) + " : " + str(value) + "\n"
jfp.close()


