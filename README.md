# CS 439 Project - Develop Test Tools Integrated with F-CIT

giraycoskun - giraycoskun@sabanciuniv.edu

cankutcoskun - cankutcoskun@sabanciuniv.edu

FCIT Project documentation is under FCIT.md

---

## Project Introduction

[Flexible Combinatorial Interaction Testing](https://ieeexplore.ieee.org/document/9144457) is present a flexible and generalized way to generate coverage arrays by defining test set as constraints.

4 test services have been developped which utilizes F-CIT to generate coverage arrays for[ Boundary Value Testing](https://en.wikipedia.org/wiki/Boundary-value_analysis) and [Masking-MCDC](https://en.wikipedia.org/wiki/Modified_condition/decision_coverage) testing approaches.

### F-CIT for Boundary Value Testing

### F-CIT for Modified Boundary Value Testing

### F-CIT for Masking-MCDC

### F-CIT for Unique-MCDC

### F-CIT for Condition based Masking-MCDC

## Usage

For the initial run "docker compose up --build"
After the initial run "docker compose up"

src/main.py script will be executed. For testing different approaches please uncomment the selected class.
Input is taken from main.py as python dictionary and output is written into result.json

For each approach a TestService Class has been implemented with a getTestSet method.

- BoundaryValueTestSeviceClass
- ModifiedBoundaryValueTestSeviceClass
- MCDCTestServiceClass
- UCMCDCTestServiceClass
- ConditionTestServiceClass

All constructed with a unique label and test space.

## References

- H. Mercan, A. Javeed and C. Yilmaz, "Flexible Combinatorial Interaction Testing," in IEEE Transactions on Software Engineering, doi: 10.1109/TSE.2020.3010317. (https://ieeexplore.ieee.org/document/9144457)

- https://cspsat.gitlab.io/sugar/package/current/docs/syntax.html

- https://cspsat.gitlab.io/sugar/

- http://www.cril.univ-artois.fr/CPAI06/descriptionSolvers/Sugar.pdf

- Hayhurst Kelly J., Veerhusen Dan S., Chilenski John J., and Rierson Leanna K. 2001. A Practical Tutorial on Modified Condition/Decision Coverage. Technical Report. NASA Langley Technical Report Server.
  (https://shemesh.larc.nasa.gov/fm/papers/Hayhurst-2001-tm210876-MCDC.pdf)
