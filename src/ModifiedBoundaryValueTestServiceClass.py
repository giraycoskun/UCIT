# Modified Condition Decision Coverage
from random import randint
from os import getcwd, walk
import subprocess

class ModifiedBoundaryValueTestSeviceClass:

    def __init__(self, request_name, test_space, single_fault=True, robust=False):
      self.input_filename = "./InputFiles/" + request_name + "_ModifiedBoundaryValueTestSevice.inFile"
      self.test_space = test_space
      self.single_fault = single_fault
      self.robust = robust
      self.entities = []

    def getTestSet(self):
        #print("FUNCTION: getTestSet")

        self.createTestSet()
        return self.__parseTestSet()

    # Parser
    def __parseTestSet(self):
        #print("FUNCTION: getTestCases")
        output_path = "./ucitObject/"
        path = walk(output_path)
        test_cases = dict()
        for _, _, files in path:
            count = 1
            for file in files:
                #print(file)
                with open(output_path+file, "r") as file:
                    lines = file.readlines()
                    check = False
                    key = "TEST CASE: "+ str(count)
                    count += 1
                    test_cases[key] = {}
                    for line in lines:
                        if check:
                            line = line.split('=')
                            test_cases[key][line[0]] = int(line[1])
                        if (not check) and line == "# TEST CASE CONSTRAINTS\n":
                            check = True
        return test_cases

    def createTestSet(self):
        #print("FUNCTION: createTestSet")
        if(not self.robust):
            self.createEntities()
            self.createInputFile(True)
        elif(self.robust):
            self.createRobustEntities()
            self.createInputFile(False)

        self.__runSolver()
        return

    def createEntities(self):
        for key, value in self.test_space.items():
            lower_constraint = key + '=' + str(value[0])
            upper_constraint = key + '=' + str(value[1])
            valid_low_constraint = key + '=' + str((value[0]+1))
            valid_up_constraint = key + '=' + str((value[1]-1))
            valid_constraint = key + '=' + str(int((value[0]+value[1])/2))
            self.entities.append(lower_constraint)
            self.entities.append(upper_constraint)
            self.entities.append(valid_low_constraint)
            self.entities.append(valid_up_constraint)
            self.entities.append(valid_constraint)

        return
    
    def createRobustEntities(self):
        for key, value in self.test_space.items():
            lower_constraint = key + '=' + str(value[0])
            upper_constraint = key + '=' + str(value[1])
            valid_low_constraint = key + '=' + str((value[0]+1))
            valid_up_constraint = key + '=' + str((value[1]-1))
            valid_constraint = key + '=' + str(int((value[0]+value[1])/2))
            invalid_low_constraint = key + '=' + str((value[0]-1))
            invalid_up_constraint = key + '=' + str((value[1]+1))
            self.entities.append(lower_constraint)
            self.entities.append(upper_constraint)
            self.entities.append(valid_low_constraint)
            self.entities.append(valid_up_constraint)
            self.entities.append(valid_constraint)
            self.entities.append(invalid_low_constraint)
            self.entities.append(invalid_up_constraint)


        return
    

    def createInputFile(self, valid=True):
        with open(self.input_filename, 'w') as file:
            self.__writeHeader(file, valid)
            for index, entity in enumerate(self.entities):
                self.__writeEntity(file, entity, index)

    def __writeHeader(self, file, valid=True):
        entity_num = len(self.entities)
        file.write("# NUMBER_OF_ENTITIES:{entity_num}\n".format(
            entity_num=entity_num))
        file.write("# SYSTEM_CONSTRAINTS_BEGIN\n")

        if(valid):
            for key, value in self.test_space.items():
                    file.write("{pNum} {lower} {upper}\n".format(pNum=key, lower=value[0], upper=value[1]))
        else:
            for key, value in self.test_space.items():
                file.write("{pNum} {lower} {upper}\n".format(pNum=key, lower=value[0]-1, upper=value[1])+1)

        file.write("# SYSTEM_CONSTRAINTS_END\n\n")

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
                   "solverUsageBased", "-i", self.input_filename]
        process = subprocess.run(command, stdout=subprocess.PIPE)
        return process.returncode
        # print(process.stdout)

test_space = {
        "time": [0, 23],
        "day": [1, 31],
        "year": [2000, 2020]
    }

if __name__ == "__main__":
    print("HEllo")
    test = ModifiedBoundaryValueTestSeviceClass("giray", test_space)
    result = test.createTestSet()
