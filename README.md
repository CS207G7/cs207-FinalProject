# cs207-FinalProject
### This is the cs207 final project repo for group 7
[![Build Status](https://travis-ci.org/CS207G7/cs207-FinalProject.svg?branch=master)](https://travis-ci.org/CS207G7/cs207-FinalProject)
[![Coverage Status](https://coveralls.io/repos/github/CS207G7/cs207-FinalProject/badge.svg?branch=master)](https://coveralls.io/github/CS207G7/cs207-FinalProject?branch=master)

### `chemkin` -- Chemical Kinetics Computational toolkit

This `chemkin` is a collection of algorithms aimed at predicting the time evolution of species concentration, finding the rate of change of a chemical species and calculating the rate of change of a certain specie. For multiple elementary reactions the rate of change follows the form:

<img src="https://github.com/CS207G7/cs207-FinalProject/blob/master/reaction_formula.jpg" width="40%">

`chemkin` is designed for flexibility, portability, easiness of use and easiness of extension. Its software design follows an object-oriented approach and its code is written on Python.


Installation
------------
1. Install the package `pip3 install cs207_g7`, and `from kinetics import chemkin`, and you can access any function you wish. Notice that for this installation method, to run the test suite, you need to navigate to the root foler of this package.
2. Clone the repo, and run `python3 setup.py install`, to run the test suite, run `python3 setup.py test`.
3. If you are interested in contributing, please ... follow the instructions.

Main Utilities
------------
### Parse raw reactions from XML

```python
parsed = chemkin.ReactionParser('path_to_reaction_xml')
```
parse the XML and obtain the following reaction details:

1. species
2. basic information, such as reaction id, reaction type, reaction equations, and etc.
3. `v1` and `v2` for each reaction

### Wrap parsed raw reactions into Reaction class
```python
reactions = chemkin.Reaction(parsed, T)
```
wrap the reactions information into a Reaction Class. Temperature T at this step.

### Obtain reaction components for each reaction
```python
V1, V2 = reactions.reaction_components()
```
since there could be multiple reactions inside a given reaction set, 
we stack each `v1` into `V1`, and each `v2` to `V2`

### Obtain reaction coeffs for each reaction
```python
k = reactions.reaction_coeff_params()
```
since the coefficient type is implicity given in the XML file. If `Arrhenius` is found, we check if `b`
is given to decide using modified or regular arr; if `Constant` is found, we use constant coeff. 
we only need user to provide T of the current reaction set, and return the list of reaction coeffs. Notice that this function can handle both reversible and non-reversible reactions. If your reaction set contains both reversible and non-reversible reactions, no worries, the function can also handle them. We will show how we handle reversible actions later.

### Obtain reaction rates for each reaction
```python
rr = chemkin.ChemKin.reaction_rate(V1, V2, X, k)
```
The last thing we need user to provide is the `X`: concentration of species. With `V1`, `V2`, and `k` computed,
user can easily obtian reaction rate for each speicies.

How to Handle Reversible Reactions
------------
### NASA polynomial coeffs
We first build up a database contains the NASA polynomial coeffs for each species. We can easily obtain the NASA coeffs for any species by
```python
get_nasa_coeffs()
```
Based on the T given, the coefficients will be extracted correspondingly.
### Enthalpy, H_over_RT
Then, we calculate the Enthalpy using the coefficients for each specie and the reaction's temperature. To obtain the Enthaply we used the following method
```python
H_over_RT()
```
Based on the T given, the Entalphy will be calculated following the form:
<img src="https://github.com/CS207G7/cs207-FinalProject/blob/master/H_over_RT_formula.JPG" width="40%">
### Entropy, S_over_T
After, we calculate the Entropy using the coefficients for each specie and the reaction's temperature. To obtain the Entropy we used the following method
```python
S_over_R()
```
Based on the T given, the Entropy will be calculated following the form:
<img src="https://github.com/CS207G7/cs207-FinalProject/blob/master/S_over_R_formula.JPG" width="40%">
### Backward Reaction Coefficients
Then, we calculated the backward reaction coefficients using the following method:
```python
backward_coeffs()
```
Based on the forward reaction rates, the backwards reaction coefficients will be calculated following the form:
<img src="https://github.com/CS207G7/cs207-FinalProject/blob/master/backward_coeffs_formula.JPG" width="40%">
### Reversible Reaction Rate
For reversible elementary reactions the rate of change follows the form:
<img src="https://github.com/CS207G7/cs207-FinalProject/blob/master/reversible_reaction_formula.JPG" width="40%">

A Complete Example
------------
The following code snippet shows an entire example that computes the reaction rate:

```python
from kinetics.chemkin import Reaction, ReactionParser, ChemKin

T = 750
X = [2, 1, 0.5, 1, 1 ,0.5, 0.5, 0.5]
reactions = Reaction(ReactionParser('your_xml'), T)
V1, V2 = reactions.reaction_components()
k = reactions.reaction_coeff_params()
rrs = ChemKin.reaction_rate(V1, V2, X, k)
print ( rrs )
```

New Feature : Centralized History!
------------
### Introduction - Motivation and Feature Description

For too long, chemists around the world have had to run all their reaction rates individually, with no idea what others were running, and no way to easily share their work. In order to save on computational complexity and runtime, we have developed a feature that records all the details of any reaction set that is run.

Our library will keep track of all elementary reactions computed by a user, and then store those in a central database for later access by not only the original user, but also anyone else around the world.

In order to make this accessible to everyone, we have developed a beautiful web interface allowing users to search based on specie, temperature, and reversible/non-reversible reactions.

We think that the feature will be really useful for scientists interested in building their own database of elementary reactions. Indeed, the devised feature allow the user to explore reactions without the need for computing again.

Our feature ultimately allows the user to find quickly the information related to the reactions already computed.

### Feature and Code Base

As the user continues to enjoy the benefits of chemkin for caulating reactions, our feature seamlessly uploads results to the central database each time chemkin is run. Our feature stores them in a database similar to the one used for NASA polynomials, but hosted on the cloud to be available for anyone. The website then allows the user to find reactions choosing among different element of interests.

#### Module: History.py

Our team has built a module `history.py`. It handles the results of each reactions computed by the user and It also stores them into a MySQL database. Thanks to the module History.py, the user is able to access the information contained in the database.

To access the history, please visit: http://54.89.19.185/app/

### Methods

The user cannot access directely to the methods because they are performed "under the hood" from our Web App which handles the user's queries. If the users want to get access to methods, he must download the package and call the methods.

### User's Experience

The user can query any information contained in the reactions that have been computed. For instance, the user can find all the reactions sort by elements of interest (e.g. type, species in the reactions, temperature of the reactions, etc). The feature allows for querying three different categories: species, reaction and temperature. After selecting the filters, and clicking the search button, the the details of the reactions that match the query will be retrieved from the cloud database. The following screenshot shows the webpage that allows for retrieving reactions from the database.

<img src="https://github.com/CS207G7/cs207-FinalProject/blob/master/webapp.jpg" width="60%">

The user can compute easily reaction rate and store them in the central database. We provide an easy API to compute and upload the results. The following code snippet shows an example:

```python

from kinetics import chemkin

T = 750

# length of X should equal to the number of species
X = [2, 1, 0.5, 1, 1 ,0.5, 0.5, 0.5] 

# this will compute the results and upload to the database automatically
compute('your/path/to/xml/file', T, X) 

```

Note that for privacy consideration, you can compute reaction rate without uploading them to the central database, to do so, just follow the example showed in the section "Example".

### External Dependencies

The history module depends primarily on a MySQL instance hosted on AWS, and a web interface built with Django and also hosted on AWS. All external libraries required for this addin at the user level (only pymysql) should be automatically installed along with cs207_g7.

### How to Run Tests

If you would like run tests, please use the following steps:
1. Clone our github repository to your local computer
2. Navigate into the cs207-FinalProject folder
3. pytest kinetics 

### How to Contribute!

If you like our work and would like to contribute to future development of ChemKin, please start by setting up a local fork of our repository, playing around with the code, and then email us at (brafetto at g.harvard.edu) with an idea of what you would like work on to request permission to contribute. A great place to start would be the list of open issues: https://github.com/CS207G7/cs207-FinalProject/issues

If you have never contributed to a github project before, feel free to look at this link for guidelines: https://akrabat.com/the-beginners-guide-to-contributing-to-a-github-project/

Or, if you'd like to contribute in other ways we also accept bitcoin 😎.
