# Modified Condition Decision Coverage
from random import randint
from os import getcwd, walk
import subprocess
import json
import re
from helper2 import Conversion

# sample = "(o1&o2|o3&-hello)&(ma|(asa7&asa1))"
# prog = re.compile("[^\(\)\&\|-]+")
# result = prog.findall(sample)
# print(result)


class UCMCDCTestServiceClass:

    OPERATORS = {'&', '|', '!'}
    PRIORITY = {
        '!':2,
        '&':1,
        '|':1,
        '(':0,
        ')':0
    }
    Converter = Conversion(OPERATORS, PRIORITY)

    def __init__(self, request_name, test_space):
        self.input_filename = "./src/InputFiles/" + \
            request_name + "_UMCDCTestInput.inFile"
        self.test_space = test_space
        self.entities = []
        self.matcher = re.compile("[^\(\)\&\|\!-]+")

    def getTestSet(self):
        #print("FUNCTION: getTestSet")

        self.createTestSet()
        return self.__parseTestSet()

    def __generateUCMCDCTestOutput(self, lines):
        #print("FUNCTION: __generateUCMCDCTestOutputestSet")
        optionID = int(lines[0].split()[-1][:-1])
        test1 = dict()
        test2 = dict()
        for line in lines[1:]:
            parsed = line.split()
            option = parsed[2]
            value = parsed[3][:-1]
            value = value[0].upper() + value[1:]
            if(option == self.test_space['options'][optionID]):
                test1[option] = eval(value)
                test2[option] = eval('not ' + value)
            else:
                test1[option] = eval(value)
                test2[option] = eval(value)

        return [test1, test2]

    # Parser
    def __parseTestSet(self):
        #print("FUNCTION: parseTestCases")
        output_path = "./ucitObject/"
        path = walk(output_path)
        test_cases = dict()
        test_set = set()
        for _, _, files in path:
            count = 1
            for file in files:
                # print(file)
                with open(output_path+file, "r") as file:
                    lines = file.readlines()

                    index = 0
                    while(lines[index] != "# TEST CASE CONSTRAINTS\n"):
                        index += 1
                    tests = self.__generateUCMCDCTestOutput(lines[index+1:])
                    for test in tests:
                        test_string = ""
                        for key, value in test.items():
                            test_string = test_string + str(key) + str(value)
                        if test_string not in test_set:
                            test_set.add(test_string)
                            key = "TEST CASE: " + str(count)
                            count += 1
                            test_cases[key] = test
                        #else:
                            #print("duplicate")

        return test_cases

    def createTestSet(self):
        #print("FUNCTION: createTestSet")
        self.createEntites()
        self.createInputFile()
        self.__runSolver()
        return self.entities

    def createEntites(self):
        for func_str in self.test_space['decisions']:
            options = self.matcher.findall(func_str)

            for option in options:
                pos_converted_function = self.Converter.infix_2_prefix(func_str)
                neg_converted_function = self.Converter.infix_2_prefix(func_str.replace(option, ('(! '+ option +')'  )))

                optionID = self.test_space['options'].index(option)
                #print("CF: ", pos_converted_function)

                pos_entity = self.Converter.formatSugarOps(
                    pos_converted_function)
                neg_entity = self.Converter.formatSugarOps(
                    neg_converted_function)

                option_entity = (
                    "\n( = optionID {optionID})".format(optionID=optionID))
                entity = "( && {pos} (! {neg}) ){op}".format(
                    pos=pos_entity, neg=neg_entity, op=option_entity)

                #print("ENTITY: ", pos_entity)
                self.entities.append(entity)
                # self.entities.append(neg_entity)

    def createInputFile(self):
        with open(self.input_filename, 'w') as file:
            self.__writeHeader(file)
            for index, entity in enumerate(self.entities):
                self.__writeEntity(file, entity, index)

    def __writeHeader(self, file):
        entity_num = len(self.entities)
        file.write("# NUMBER_OF_ENTITIES:{entity_num}\n".format(
            entity_num=entity_num))
        file.write("# SYSTEM_CONSTRAINTS_BEGIN")

        file.write("\n(int optionID 0 {entity_num} )".format(
            entity_num=entity_num))

        for option in self.test_space['options']:
            file.write('\n(bool ' + option + ')')

        file.write("\n# SYSTEM_CONSTRAINTS_END\n\n")

    def __writeEntity(self, file, entity, entityID, description=""):
        description = 'Covering ' + entity.split('\n')[0]
        file.write("# ENTITY_BEGIN\n")
        file.write("# ENTITY_ID:{entityID}\n".format(entityID=entityID))
        file.write("# ENTITY_DESCRIPTION: {description}\n".format(
            description=description))
        #print("\nENTITY: ", entity)
        file.write(entity)
        file.write("\n")
        file.write("# ENTITY_END\n\n")

    def __runSolver(self):
        # "python main.pyc -m 1 -s solverOrderBased -i ./sampleInputFiles/solverBased.inFile"
        command = ["python", "main.pyc", "-m", "1", "-s",
                   "solverOrderBased", "-i", self.input_filename]
        process = subprocess.run(command, stdout=subprocess.PIPE)
        return process.returncode
        # print(process.stdout)


sample_MCDC_test_space = {

    "options": ["o1", "o2", "o3"],
    "functions": [
        "(o1|(o2&o3))"
    ]
}

sample_MCDC_test_space = {

    "options": ["o1"],
    "functions": [
        "(o1)"
    ]
}

sample_MCDC_test_space = {

    "options": ["o1", "o2"],
    "functions": [
        "(o1&o2)"
    ]
}

sample_MCDC_test_space = {

    "options": ["o1", "o2"],
    "functions": [
        "(o1|o2)"
    ]
}

MCDC_test_space = {

    "options": ["o1", "o2", "o3"],
    "decisions": [
        "(o1&o2&o3)"
    ]
}

sample_MCDC_test_space = {

    "options": ["o1", "o2", "o3"],
    "decisions": [
        "(o1&o2&o3)",
        "(o1|(o2&o3))"
    ]
}

if __name__ == "__main__":
    #print("HEllo")
    test = UCMCDCTestServiceClass("giray", MCDC_test_space)
    result = test.getTestSet()
    #print(result)
