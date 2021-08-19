from py_expression_eval import Parser
from os import walk, getcwd, chdir
from subprocess import Popen, PIPE
import re
from  util import Conversion
import logging
import sys
from json import dump
log_level = logging.INFO

logging.basicConfig(stream=sys.stdout)
log = logging.getLogger(__name__)
log.setLevel(log_level)

util_logger = logging.getLogger('util')
util_logger.setLevel(log_level)

TOOL_DIRECTORY = "./src/tool/"
UCIT_OBJECT_DIRECTORY = TOOL_DIRECTORY + "ucitObject/"

class MaskingMCDCTest:
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
        self.input_filename = "./src/MaskingMCDC-Input-Tool-Files/" + request_name + "_ConditonBasedTestInput.inFile"
        self.output_filename = "./src/MaskingMCDC-Output-Files/" + request_name + "_ConditonBasedTestInput.outFile"
        self.test_space = test_space
        self.entities = []
        self.options = []
        self.matcher = re.compile("[\|\&\!)( ]")

    def getTestSet(self):
        self.createTestSet()
        return self.__parseTestSet()


    def createTestSet(self):
        self.createEntites()
        self.createInputFile()
        self.__runSolver()
        return self.entities
    
    def createEntites(self):
        for decision in self.test_space['decisions']:
            log.debug(decision)
            function = decision[0]
            log.debug("Function: " + function)
            options = self.matcher.split(function)
            options = list(filter(lambda option: option not in {'&', '|', '!', '(', ')', '', ' '}, options))
            func_str = ""
            for element in decision:
                func_str = func_str + element + '&'
            func_str = func_str[:-1]
            log.debug("Function under nested conditions: " + func_str)
            for option in options:
                if option not in self.options:
                    self.options.append(option)
                pos_converted_function = self.converter.infix_2_prefix(func_str)
                indexes = [i for i in range(len(func_str)) if func_str.startswith(option, i)]
                res_index = -1
                for index in indexes:
                    try:
                        if not(func_str[index + len(option)].isnumeric()):
                            res_index = index
                    except Exception:
                        res_index = index
                    break
                func_str = func_str[:res_index] + func_str[res_index:].replace(option, '(!'+option +')', 1)
                neg_converted_function = self.converter.infix_2_prefix(func_str)
                
                pos_func = self.converter.formatSugarOps(pos_converted_function)
                neg_func = self.converter.formatSugarOps(neg_converted_function)


                pos_entity = "( && {pos} (! {neg}) )".format(pos=pos_func, neg=neg_func)
                neg_entity = "( && {neg} (! {pos}) )".format(pos=pos_func, neg=neg_func)
                self.entities.append((pos_entity, decision))
                self.entities.append((neg_entity, decision))

    def createInputFile(self):
        with open(self.input_filename, 'w') as file:
            self.__writeHeader(file)
            for index, entity in enumerate(self.entities):
                self.__writeEntity(file, entity, index+1)

    def __writeHeader(self, file):
        entity_num = len(self.entities)
        file.write("# NUMBER_OF_ENTITIES:{entity_num}\n".format(
            entity_num=entity_num))
        file.write("# SYSTEM_CONSTRAINTS_BEGIN")

        for option in self.test_space['options']:
            file.write('\n(bool ' + option + ')')
        
        for key, value in self.test_space['numbers'].items():
            file.write('\n(int {number} {lower} {upper} )'.format(number=key, lower=value[0], upper=value[1]))

        file.write("\n# SYSTEM_CONSTRAINTS_END\n\n")

    def __writeEntity(self, file, entity, entityID):
        description = 'Covering {}'.format(" ".join(entity[1]))
        file.write("# ENTITY_BEGIN\n")
        file.write("# ENTITY_ID:{entityID}\n".format(entityID=entityID))
        file.write("# ENTITY_DESCRIPTION: {description}\n".format(description=description))
        file.write(entity[0])
        file.write("\n")
        file.write("# ENTITY_END\n\n")

    def __runSolver(self):
        current_directory = getcwd()
        chdir(TOOL_DIRECTORY)
        log.debug(getcwd)
        # "python main.pyc -m 1 -s solverOrderBased -i ./sampleInputFiles/solverBased.inFile"
        input_name = "../../" + self.input_filename
        command = ["python", "tool.pyc", "-m", "1", "-s",
                   "solverOrderBased", "-i", input_name]
        with open("stdout.txt","wb") as out, open("stderr.txt","wb") as err:
            process = Popen(command, stdout=out, stderr=err).wait() #process = subprocess.run(command, stdout=subprocess.PIPE)
        chdir(current_directory)
        log.debug(getcwd)
        if(process != 0):
            log.warning("U-CIT FAILED generating test cases")
        return process

    def __parseTestSet(self):
        output_path = "./src/tool/ucitObject/"
        path = walk(output_path)
        test_cases = dict()
        for _, _, files in path:
            count = 1
            for file in files:
                #print(file)
                with open(output_path+file, "r") as file:
                    lines = file.readlines()

                    index = 0
                    while(lines[index] !=  "# TEST CASE CONSTRAINTS\n" ):
                        index += 1
                    key = "TEST CASE: "+ str(count)
                    count += 1
                    test_cases[key] = self.__generateTestOutput(lines[index+1:])
        return test_cases
    
    def __generateTestOutput(self, lines):
        test = dict()
        for line in lines:
            parsed = line.split()
            option = parsed[2]
            value = parsed[3][:-1]
            if value in {'true', 'false'}:
                value = value[0].upper() + value[1:]
            
            test[option] = eval(value)
        return test

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
        
    tester = MaskingMCDCTest('test_g1', test_input_1)
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