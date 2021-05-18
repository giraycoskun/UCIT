import BoundaryValueTestSeviceClass as BVC

sample_test_space = {
    "time": [1, 4],
    "day": [-4, 105],
    "year": [-4, 105]
}

testService = BVC.BoundaryValueTestSeviceClass("giray", sample_test_space)
result = testService.getTestSet()

print(result)