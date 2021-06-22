import BoundaryValueTestSeviceClass as BVC
import ModifiedBoundaryValueTestServiceClass as MBVC
import MCDCTestServiceClass as MCDC
import UCMCDCTestServiceClass as UCMCDC
import ConditionTestServiceClass as ConditionTestClass

import json

##INPUT TEST SPACE
dir_name = "./src/InputObjects/"
object_name = "dia"
filename = dir_name + object_name + ".json"

with open(filename, 'r') as fp:
    test_space = json.load(fp)


'''
#UC-MCDC
test_service = UCMCDC.UCMCDCTestServiceClass(object_name, test_space)
result = test_service.getTestSet()

print(result)

dir_name = "./src/OutputObjects/"
object_name = "dia"
filename = dir_name + object_name + "_UCMCDC_result.json"
with open(filename, 'w') as fp:
    json.dump(result, fp)
'''


#MCDC Condition

test_service = ConditionTestClass.ConditionTestServiceClass(object_name, test_space)
result = test_service.getTestSet()

print(result)

dir_name = "./src/OutputObjects/"
object_name = "dia"
filename = dir_name + object_name + "_MCDC_result.json"
with open(filename, 'w') as fp:
    json.dump(result, fp)


'''

boundary_test_case = {
        "time": [1, 4],
        "day": [-4, 105],
        "year": [-4, 105]
    }

mcdc_test_cases = [
{
    "options": ["o1", "o2","o3","o4"],
    "functions": [
        "(o1&o2)",
        "(o3|o4)"
    ]
},
{

    "options": ["o1", "o2", "o3"],
    "functions": [
        "(o1|(o2&o3))"
    ]
},

{

    "options": ["o1"],
    "functions": [
        "(o1)"
    ]
},

{

    "options": ["o1", "o2"],
    "functions": [
        "(o1&o2)"
    ]
},

{

    "options": ["o1", "o2"],
    "functions": [
        "(o1|o2)"
    ]
},

{

    "options": ["o1", "o2", "o3"],
    "functions": [
        "(o1&o2&o3)"
    ]
},

{

    "options": ["o1", "o2", "o3"],
    "functions": [
        "(o1&o2&o3)",
        "(o1|(o2&o3))"
    ]
}   
]

test_space = {

    "options": ["o1", "o2", "o3"],
    "functions": [
        "(o1|(o2&o3))"
    ]
}

condition_test_space = {
    
        "conditions":[
            "(a<b+e)|(c<d)&!x",
            "o1&o2"
        ],

        "numbers": {
            "a":[1, 20],
            "b":[1, 100],
            "c":[1, 20],
            "d":[1, 100],
            "e":[1, 100]
        }
        ,
        "options": ['x', 'y', 'o1', 'o2']
    }

#testService = BVC.BoundaryValueTestSeviceClass("giray", boundary_test_case)
#testService = MBVC.ModifiedBoundaryValueTestSeviceClass("giray", boundary_test_case)
#testService = BVC.BoundaryValueTestSeviceClass("giray", boundary_test_case, True, True)
#testService = MCDC.MCDCTestServiceClass("cankut", test_space)
#testService = UCMCDC.UCMCDCTestServiceClass("Giray", test_space)
#testService = ConditionTestClass.ConditionTestServiceClass("giray", condition_test_space)
#result = testService.getTestSet()

print(result)
with open('./src/result.json', 'w') as fp:
    json.dump(result, fp)
'''