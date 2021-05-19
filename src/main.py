import BoundaryValueTestSeviceClass as BVC
import json

sample_test_space = {
    "time": [1, 4],
    "day": [-4, 105],
    "year": [-4, 105]
}

sample_MCDC_test_space = {


    "options":["o1", "o2"],
    "functions": [ 
        "o1&o2",
        "o3|o4",
        "()"
    ]
}

##
testService = BVC.BoundaryValueTestSeviceClass("giray", sample_test_space)
result = testService.getTestSet()
print(result)
with open('createBoundaryValueTestInput.json', 'w') as fp:
    json.dump(result, fp)

##
testService = BVC.BoundaryValueTestSeviceClass("giray", sample_test_space, True, True)
result = testService.getTestSet()
print(result)
with open('createRobustBoundaryValueTestInput.json', 'w') as fp:
    json.dump(result, fp)