#!/usr/bin/python -u

import os
import re
import json
import tempfile
import traceback
from pprint import pprint


with open('centos.json') as data_file:
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
    print "//-----------------------------------"
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
    print "//-----------------------------------"
    for key, value in section.iteritems():
        print "\t" + str(key) + " : " + str(value)
    printFooter()
'''  
def processProvisioners(section=''):
    '''
    '''
    printHeader()
    print "//# provisioners                         #"
    print "//-----------------------------------"
    for item in section:
        for key, value in item.iteritems():
            print "\t" + str(key) + " : " + str(value)
    printFooter()


if __name__ == "__main__":

    newJson = {}

    try:
        newJson['_comment'] = data["_comment"]
    except KeyError, err:
        print traceback.format_exc()
        newJson['_command'] = data['_command']

    newJson['variables'] = data['variables']
    newJson['provisioners'] = data['provisioners']
    newJson['builders'] = []

    vmtypes = ['vmware-iso', 'virtualbox-iso']
    includeVagrant = False

    for key, values in data.iteritems():
        if re.match("builders", key):
            #print str(values)
            for item in values:
                print item['type']
                if item['type'] in vmtypes:
                    newJson['builders'].append(item)

        elif re.match("post-processors", key) and includeVagrant:
            newJson[key] = data[key]

    for key, value in newJson.iteritems():
        if re.match("_comment", key) or re.match('_command', key):
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


