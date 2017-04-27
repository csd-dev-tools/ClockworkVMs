#!/usr/bin/python

import json

jfp = open("centos.json", "r")
jstuff = json.load(jfp)
print "\n========================================="
for key, value in jstuff.iteritems():
    print str(key) + " : " + str(value) + "\n"

print "---"
print "\nPost Processors:\n"
for value in jstuff["post-processors"]:
    print str(value) + "\n"

print "---"
print "\nBuilders:\n"
for value in jstuff["builders"]:
    print str(value) + "\n"

print "---"
print "\nProvisioners:\n"
for value in jstuff["provisioners"]:
    print str(value) + "\n"

print "---"
print "\nVariables\n"
for key, value in jstuff["variables"].iteritems():
    print str(key) + " : " + str(value)

jfp.close()

