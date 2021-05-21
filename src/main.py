import BoundaryValueTestSeviceClass as BVC
import ModifiedBoundaryValueTestServiceClass as MBVC
import MCDCTestServiceClass as MCDC
import json

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

#testService = BVC.BoundaryValueTestSeviceClass("giray", boundary_test_case)
#testService = MBVC.ModifiedBoundaryValueTestSeviceClass("giray", boundary_test_case)
#testService = BVC.BoundaryValueTestSeviceClass("giray", boundary_test_case, True, True)
testService = MCDC.MCDCTestServiceClass("cankut", test_space)
result = testService.getTestSet()
print(result)
with open('./src/result.json', 'w') as fp:
    json.dump(result, fp)
