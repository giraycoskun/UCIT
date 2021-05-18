from typing import no_type_check_decorator
import json
import subprocess
from os import getcwd, walk
from random import randint

class BoundaryValueTestSeviceClass:
    

    def __init__(self, request_name, test_space, single_fault=True, robust=False):
      self.input_filename = "./InputFiles/" + request_name + "_createBoundaryValueTestInput.inFile"
      self.test_space = test_space
      self.single_fault = single_fault
      self.robust = robust

    
    def getTestSet(self):
        print("FUNCTION: getTestSet")
        if(self.single_fault and (not self.robust)):
            self.createBoundaryValueTestInput()
        
        return self.__getTestCases()

    def __getTestCases(self):
        print("FUNCTION: getTestCases")
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
                        

        

    def createBoundaryValueTestInput(self):
        print("FUNCTION: createBoundaryValueTestInput")
        self.__writeSingleFaultRanges()

        with open(self.input_filename, 'a') as file:

            entityID = 1

            randomValues = dict()
            for key, value in self.test_space.items():
                randomValues[key] = randint(value[0], value[1])

            self.__writeEntity(file, randomValues, entityID, "regular")
            entityID += 1
            
            for key, value in self.test_space.items():
                values = randomValues
                values[key] = value[0]
                self.__writeEntity(file, values, entityID, str(key)+" lower-bound")
                values[key] = value[1]
                self.__writeEntity(file, values, entityID+1, str(key)+" upper-bound")
                entityID += 2

        self.__runSolver()
        return dict()

    def createRobustBoundaryValueTestInput(self):
        print("FUNCTION: createRobustBoundaryValueTestInput")
        return dict()

    def createWorstCaseBoundaryValueTestInput(self):
        pass

    def createWorstCaseRobustBoundaryValueTestInput(self):
        pass

    def __writeSingleFaultRanges(self):
        parameterNum = len(self.test_space.keys())*2 + 1
        with open(self.input_filename, 'w') as file:

            file.write("# NUMBER_OF_ENTITIES:{parameterNumber}\n".format(parameterNumber = parameterNum))
            file.write("# SYSTEM_CONSTRAINTS_BEGIN\n")

            for key, value in self.test_space.items():
                file.write("{pNum} {lower} {upper}\n".format(pNum=key, lower=value[0], upper=value[1]))

            file.write("# SYSTEM_CONSTRAINTS_END\n\n")

    def __writeEntity(self, file, values, entityID, description=""):

        file.write("# ENTITY_BEGIN\n")
        file.write("# ENTITY_ID:{entityID}\n".format(entityID=entityID))
        file.write("# ENTITY_DESCRIPTION: {description}\n".format(description=description))
        parameter_string = ""
        for key, value in values.items():
            parameter_string += "{pNum}={value},".format(pNum=key, value=value)
        file.write(parameter_string[:-1])
        file.write("\n")
        file.write("# ENTITY_END\n\n")

    def __runSolver(self):
        #"python main.pyc -m 1 -s solverUsageBased -i ./sampleInputFiles/usageBasedStudy.inFile"
        command = ["python", "main.pyc", "-m", "1", "-s", "solverUsageBased", "-i", self.input_filename]
        process = subprocess.run(command, stdout=subprocess.PIPE)
        return process.returncode
        #print(process.stdout)



sample_test_space = {
    "time": [1, 4],
    "day": [-4, 105],
    "year": [-4, 105]
}

if __name__ == "__main__":
    print("HEllo")
    with open("sample_input.json", "w") as file:
        file.write(json.dumps(sample_test_space))
    with open("sample_input.json", "r") as file:
        data = json.load(file)
    print(data)
    test = BoundaryValueTestSeviceClass("giray", sample_test_space)
    result = test.createBoundaryValueTestInput()
