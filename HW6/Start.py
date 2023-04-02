import sys, getopt
from Examples import *

argumentList = sys.argv[1:]
the = {"seed": 937162211, "dump": False, "halves":"", "reuse":True , "go": "data", "help": False, "file": "/etc/data/repgrid1.csv","min": "min", "rest":4}
b4={}
ENV = {}
for k,v in ENV:
    b4[k]=v #cache old names (so later, we can find rogues)
# Options
options = "hg"
 
# Long options
long_options = []
def help():
    a= """
        script.lua : an example script with help text and a test suite
        (c)2022, Tim Menzies <timm@ieee.org>, BSD-2
        USAGE:   script.lua  [OPTIONS] [-g ACTION]
        OPTIONS:
        -d  --dump    on crash, dump stack   = false
        -f  --file    name of file           = ../etc/data/repgrid1.csv
        -g  --go      start-up action        = data
        -h  --help    show help              = false
        -p  --p       distance coefficient   = 2
        -s  --seed    random number seed     = 937162211
        ACTIONS:
        -g  the	show settings
        -g  rand	generate, reset, regenerate same
        -g  sym	check syms
        -g  num	check nums
        """
    print(a)


def run_tests():
    func_pass= 0
    test_suite = [test_nums, test_sym,test_the, test_half, test_csv, test_data,  test_clone, test_cliffs, test_tree,  test_dist, test_csv, test_sway, test_bins, test_explain] 
    # test_suite = [test_explain]
    for i,test in enumerate(test_suite):
        if(test()):
            func_pass += 1
    print("\nTotal Test Cases Passing: " + str(func_pass) + "\nTotal Test Cases Failing: " + str(len(test_suite)-func_pass))
    

def main():
    try:
        arguments, values = getopt.getopt(argumentList, options, long_options)
        for currentArgument, currentValue in arguments:
             if currentArgument in ('-h', ''):
                help()
             if currentArgument in ("-g", ''):
               run_tests() 
                
    except getopt.error as err:
        print (str(err))

if __name__ == "__main__":
  main()