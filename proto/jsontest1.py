#!/usr/bin/python -u

import re
import json
from pprint import pprint



with open('macos.json') as data_file:
    data = json.load(data_file)
pprint(data)



def printHeader():
    '''
    '''
    print "//########################################"
    print "//#                                      #"

def printFooter():
    '''
    '''
    print "//#                                      #"
    print "//########################################"

def processComments(section=''):
    '''
    '''
    printHeader()
    print "//# comments                             #"
    print str(section)
    printFooter()
 
def processPostProcessors(section=''):
    '''
    '''
    printHeader()
    print "//# post-processors create vagrant box...#"
    for item in section:
        print item
    printFooter()

def processBuilders(section=''):
    '''
    '''
    printHeader()
    print "//# builders                             #"
    for item in section:
        print "//-----------------------------------"
        print "// === Type: " + item['type'] + "\n"
        for key, value in item.iteritems():
            print "\t" + str(key) + " : " + str(value) + "\n"
    printFooter()
     
'''
def processVariables(section=''):
    printHeader()
    print "//# variables                            #"
    for key, value in section.iteritems():
        print "\t" + str(key) + " : " + str(value)
    printFooter()
 '''    
def processProvisioners(section=''):
    '''
    '''
    printHeader()
    print "//# provisioners                         #"
    for item in section:
        for key, value in item.iteritems():
            print "\t" + str(key) + " : " + str(value)
    printFooter()


if __name__ == "__main__":

    for key, value in data.iteritems():
        if re.match("_comment", key):
            processComments(value)

        if re.match("post-processors", key):
            processPostProcessors(value)

        if re.match("builders", key):
            processBuilders(value)
        '''
        if re.match("variables", key):
            processVariables(value)
        '''
        if re.match("provisioners", key):
            processProvisioners(value)


