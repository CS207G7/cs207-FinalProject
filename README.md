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

Download the package, and `from chemkin import *`, and you can access any function you wish.


Main Utilities
------------
### 1. Parse raw reactions from XML

```python
parsed = ReactionParser('path_to_reaction_xml')
```
parse the XML and obtain the following reaction details:

1. species
2. basic information, such as reaction id, reaction type, reaction equations, and etc.
3. `v1` and `v2` for each reaction

### 2. Wrap parsed raw reactions into Reaction class
```python
reactions = Reaction(parsed, T)
```
wrap the reactions information into a Reaction Class. Temperature T at this step.

### 3. Obtain reaction components for each reaction
```python
V1, V2 = reactions.reaction_components()
```
since there could be multiple reactions inside a given reaction set, 
we stack each `v1` into `V1`, and each `v2` to `V2`

### 4. Obtain reaction coeffs for each reaction
```python
k = reactions.reaction_coeff_params()
```
since the coefficient type is implicity given in the XML file. If `Arrhenius` is found, we check if `b`
is given to decide using modified or regular arr; if `Constant` is found, we use constant coeff. 
we only need user to provide T of the current reaction set, and return the list of reaction coeffs. Notice that this function can handle both reversible and non-reversible reactions. If your reaction set contains both reversible and non-reversible reactions, no worries, the function can also handle them. We will show how we handle reversible actions later.

### 5. Obtain reaction rates for each reaction
```python
rr = ChemKin.reaction_rate(V1, V2, X, k)
```
The last thing we need user to provide is the `X`: concentration of species. With `V1`, `V2`, and `k` computed,
user can easily obtian reaction rate for each speicies.

How to Handle Reversible Actions
------------
### 1. NASA polynomial coeffs
We first build up a database contains the NASA polynomial coeffs for each species. We can easily obtain the NASA coeffs for any species by
```python
get_nasa_coeffs(specie, T)
```
Based on the T given, the coefficients will be extracted correspondingly.
### 2. Enthalpy, H_over_RT
Then, we calculate the Enthalpy using the coefficients for each specie and the reaction's temperature. To obtain the Enthaply we used the following method
```python
H_over_RT(nasa_coeffs, T)
```
Based on the T given, the Entalphy will be calculated accordingely.
### 3. Entropy, S_over_T
After, we calculate the Entropy using the coefficients for each specie and the reaction's temperature. To obtain the Entropy we used the following method
```python
S_over_R(nasa_coeffs, T)
```
Based on the T given, the Entropy will be calculated accordingely.
### 4. Backward Reaction Coefficients
Then, we calculated the backward reaction coefficients using the following method that requires as inputs `H_over_RT`, `S_over_R`,  `v1`, `v2` 
```python
backward_coeffs(H_over_RT, S_over_R, V1, V2, rr)
```
Based on the forward reaction rates (`rr`) the backwards reaction coefficients will be calculated.
### 5. Reversible Reaction Rate
For reversible elementary reactions the rate of change follows the form:
<img src="https://github.com/CS207G7/cs207-FinalProject/blob/master/reversible_reaction_formula.jpg" width="40%">

Future Features
------------
