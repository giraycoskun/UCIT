# Modified Condition Decision Coverage
from random import randint
from os import getcwd, walk
import subprocess
import json
from typing import no_type_check_decorator
import re

# sample = "(o1&o2|o3&-hello)&(ma|(asa7&asa1))"
# prog = re.compile("[^\(\)\&\|-]+")
# result = prog.findall(sample)
# print(result)


class MCDCTestServiceClass:

    def __init__(self, request_name, test_space):
        self.input_filename = "./InputFiles/" + \
            request_name + "_createMCDCTestInput.inFile"
        self.test_space = test_space
        self.entities = []
        self.matcher = re.compile("[^\(\)\&\|-]+")

    def getTestSet(self):
        print("FUNCTION: getTestSet")

        self.createTestSet()
        return self.__parseTestSet()

    # Parser
    def __parseTestSet(self):
        print("FUNCTION: __parseTestSet")
        output_path = "./ucitObject/"
        path = walk(output_path)
        test_cases = dict()
        for _, _, files in path:
            for file in files:
                with open(output_path+file, "r") as file:
                    lines = file.readlines()
                    check = False
                    key = lines[0].strip()
                    test_cases[key] = {}
                    for line in lines:
                        if check:
                            line = line.split('=')
                            test_cases[key][line[0]] = int(line[1])
                        if (not check) and line == "# TEST CASE CONSTRAINTS\n":
                            check = True
        return test_cases

    def createTestSet(self):
        print("FUNCTION: createTestSet")
        self.createEntites()
        self.createInputFile()
        self.__runSolver()
        return self.entities

    def createEntites(self):
        for func_str in self.test_space['functions']:
            options = self.matcher.findall(func_str)
            for option in options:
                # (option) & (function)
                # (-option) & (-function)
                pos_entity = '(' + option + ')&' + func_str
                neg_entity = '(-' + option + ')&(-' + func_str + ')'
                self.entities.append(pos_entity)
                self.entities.append(neg_entity)

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

        for option in self.test_space['options']:
            file.write('\n' + option)

        file.write("\n# SYSTEM_CONSTRAINTS_END\n\n")

    def __writeEntity(self, file, entity, entityID, description=""):
        description = 'Covering ' + entity
        file.write("# ENTITY_BEGIN\n")
        file.write("# ENTITY_ID:{entityID}\n".format(entityID=entityID))
        file.write("# ENTITY_DESCRIPTION: {description}\n".format(
            description=description))
        file.write(entity)
        file.write("\n")
        file.write("# ENTITY_END\n\n")

    def __runSolver(self):
        # "python main.pyc -m 1 -s solverStructuredBased -i ./sampleInputFiles/structuredBased.inFile"
        command = ["python", "main.pyc", "-m", "1", "-s",
                   "solverStructureBased", "-i", self.input_filename]
        process = subprocess.run(command, stdout=subprocess.PIPE)
        return process.returncode
        # print(process.stdout)


sample_MCDC_test_space = {

    "options": ["o1", "o2", "o3"],
    "functions": [
        "(o1|(o2&o3))"
    ]
}

if __name__ == "__main__":
    print("HEllo")
    test = MCDCTestServiceClass("cankut", sample_MCDC_test_space)
    result = test.createTestSet()
