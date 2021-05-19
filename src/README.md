# CS 439 Project - Develop Test Tools Integrated with F-CIT

giraycoskun - giraycoskun@sabanciuniv.edu

cankutcoskun - cankutcoskun@sabanciuniv.edu

---

## Project Introduction

[Flexible Combinatorial Interaction Testing](https://ieeexplore.ieee.org/document/9144457) is present a flexible and generalized way to generate coverage arrays by defining test set as constraints.

2 test services have been developped which utilizes F-CIT to generate coverage arrays for[ Boundary Value Testing](https://en.wikipedia.org/wiki/Boundary-value_analysis) and [Masking-MCDC](https://en.wikipedia.org/wiki/Modified_condition/decision_coverage) testing approaches.

### F-CIT for Boundary Value Testing

### F-CIT for Masking-MCDC

## Usage

For each approach a TestService Class has been implemented with a getTestSet method.

- BoundaryValueTestSeviceClass
- MCDCTestServiceClass

Both constructued with a unique request name and test space.


## References

- H. Mercan, A. Javeed and C. Yilmaz, "Flexible Combinatorial Interaction Testing," in IEEE Transactions on Software Engineering, doi: 10.1109/TSE.2020.3010317. (https://ieeexplore.ieee.org/document/9144457)
