import logging
import re
import sys
from util import Conversion
from os import getcwd
from json import dump

TOOL_DIRECTORY = "./src/tool_seed/"
UCIT_OBJECT_DIRECTORY = TOOL_DIRECTORY + "ucitObject/"
log_level = logging.INFO

logging.basicConfig(stream=sys.stdout)
log = logging.getLogger(__name__)
log.setLevel(log_level)

class UniqueCauseMCDCTest:
    OPERATORS = {'&', '|', '!', '<', '>', '+', '-', '*', '/'}
    PRIORITY = {
        '*':5,
        '/':5,
        '-':4,
        '+':4,
        '>':3,
        '<':3,
        '!':2,
        '&':1,
        '|':1,
        '(':0,
        ')':0
    }

    converter = Conversion(OPERATORS, PRIORITY)

    def __init__(self, request_name, test_space):
        self.input_filename = "./src/UniqueCauseMCDC-Input-Tool-Files/" + request_name + ".inFile"
        self.output_filename = "./src/UniqueCauseMCDC-Output-Files/" + request_name + ".outFile"
        self.test_space = test_space
        self.entities = []
        self.options = []
        self.matcher = re.compile("[\|\&\!)(]")

    def getTestSet(self):
            self.createTestSet()
            return self.__parseTestSet()
    
    def dumpTests(self, tests):
        with open(self.output_filename, 'w') as output_file:
            dump(tests, output_file, indent = 8)




if __name__ == '__main__':
    log.info("START")
    log.info("Current workdir: " + getcwd())
    test_input_0  = \
        {
            "decisions":[
                ["o1&o3", ],
                ["o2", "!(o1&o3)"],

                ["((o3))", ],
                ["o4", "!o3"],
                ["o2", "!o3", "o4"]

            ],

            "options": ["o1", "o2", "o3", "o4"],
            "numbers": {}
        }

    test_input_1  = \
        {
            "decisions":[
                ["o1&o3", ],
                ["o2", "!(o1&o3)"],

                ["((o3))", ],
                ["o4", "!o3"],
                ["o2", "!o3", "o4"],

                ["a>b & c<d"]

            ],

            "options": ["o1", "o2", "o3", "o4"],
            "numbers": {
                            "a":[1, 20],
                            "b":[1, 100],
                            "c":[1, 20],
                            "d":[1, 100]
                        }
        }
        
    tester = UniqueCauseMCDCTest('test_g0', test_input_0)
    tests = tester.getTestSet()
    tester.dumpTests(tests)
    log.info("Tests Are Generated")

    
    

'''
test_input_0
// v2; 1
    #if ((o1&o3)) {
	    } 
    else {
        if ((o2)) {

        } 
        else {
        }
	}
// v2; 2
    #if ((o3)) {
    } else {
        if ((o4)) {
            if(o2){

            }
        }
    }
'''