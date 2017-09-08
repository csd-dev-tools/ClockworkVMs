#!/usr/bin/python

import os, sys
from optparse import OptionParser
from optparse import Option, OptionValueError

version = "0.9.4.11"

class MultipleOptions(Option):
    ACTIONS = Option.ACTIONS + ("extend",)
    STORE_ACTIONS = Option.STORE_ACTIONS + ("extend",)
    TYPED_ACTIONS = Option.TYPED_ACTIONS + ("extend",)
    ALWAYS_TYPED_ACTIONS = Option.ALWAYS_TYPED_ACTIONS + ("extend",)

    def take_action(self, action, dest, opt, value, values, parser):
        if action == "extend":
            lvalue = value.split(",")
            values.ensure_value(dest, []).append(value)
        else:
            Option.take_action(self, action, dest, opt, value, values, parser)

def main():
    program_name = __file__
    long_commands = ("exclude_files", "exclude_from_line")
    short_commands = {"exfl" : "exclude_files", "exlw" : "exclude_lines_with"}
    description = "Process files and lines except excluded ones..." + \
                  "./multiple_options.py --exclude_files one -f two " +\
                  "--exclude_lines_with four -l five arg1 arg2" +\
                  "\nArguments: ['arg1', 'arg2']"+\
                  "\nOptions  : {'excludeFiles': ['one', 'two'], " +\
                  "'excludeLinesWith': ['four', 'five']}\n"
                  
    parser = OptionParser(option_class=MultipleOptions,
                          usage="usage: %prog [OPTIONS] COMMAND",
                          version="%s, %s"%(program_name, version),
                          description=description)

    parser.add_option("-f", "--exclude_files",
                      action="extend", type="string",
                      dest="excludeFiles",
                      metavar="EXCLUDEFILES",
                      help="comma separated list of strings to use to exclude lint errors.  Also can have multiple -f, each with it's own file name string to exclude.")

    parser.add_option("-l", "--exclude_lines_with",
                      action="extend", type="string",
                      dest="excludeLinesWith",
                      metavar="EXCLUDELINESWITH",
                      help="comma separated list of strings to use to exclude lint errors.  Also can have multiple -l, each with it's own string to exlude.")

    if len(sys.argv) < 2:
        parser.parse_args(["--help"])

    opts, args = parser.parse_args()
    print "Arguments: " + str(args)
    print "Options  : " + str(opts)
    
    print opts.excludeLinesWith
    print opts.excludeFiles

if __name__=="__main__":
    main()
