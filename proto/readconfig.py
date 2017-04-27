#!/usr/bin/python

from ConfigParser import SafeConfigParser

# lets create that config file for next time...
cfgfile = open("next.ini",'w')
parser = SafeConfigParser()

# add the settings to the structure of the file, and lets write it out...
parser.add_section('Person')
parser.set('Person','HasEyes','True')
parser.set('Person','Age', '50')
parser.write(cfgfile)
cfgfile.close()

