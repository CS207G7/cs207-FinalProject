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

Install the package `pip3 install chemkin`, and `from kinetics import chemkin`, and you can access any function you wish.


Main Utilities
------------
### 1. Parse raw reactions from XML

```python
parsed = chemkin.ReactionParser('path_to_reaction_xml')
```
parse the XML and obtain the following reaction details:

1. species
2. basic information, such as reaction id, reaction type, reaction equations, and etc.
3. `v1` and `v2` for each reaction

### 2. Wrap parsed raw reactions into Reaction class
```python
reactions = chemkin.Reaction(parsed, T)
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
rr = chemkin.ChemKin.reaction_rate(V1, V2, X, k)
```
The last thing we need user to provide is the `X`: concentration of species. With `V1`, `V2`, and `k` computed,
user can easily obtian reaction rate for each speicies.

How to Handle Reversible Actions
------------
### 1. NASA polynomial coeffs
We first build up a database contains the NASA polynomial coeffs for each species. We can easily obtain the NASA coeffs for any species by
```python
get_nasa_coeffs()
```
Based on the T given, the coefficients will be extracted correspondingly.
### 2. Enthalpy, H_over_RT
Then, we calculate the Enthalpy using the coefficients for each specie and the reaction's temperature. To obtain the Enthaply we used the following method
```python
H_over_RT()
```
Based on the T given, the Entalphy will be calculated following the form:
<img src="https://github.com/CS207G7/cs207-FinalProject/blob/master/H_over_RT_formula.JPG" width="40%">
### 3. Entropy, S_over_T
After, we calculate the Entropy using the coefficients for each specie and the reaction's temperature. To obtain the Entropy we used the following method
```python
S_over_R()
```
Based on the T given, the Entropy will be calculated following the form:
<img src="https://github.com/CS207G7/cs207-FinalProject/blob/master/S_over_R_formula.JPG" width="40%">
### 4. Backward Reaction Coefficients
Then, we calculated the backward reaction coefficients using the following method:
```python
backward_coeffs()
```
Based on the forward reaction rates, the backwards reaction coefficients will be calculated following the form:
<img src="https://github.com/CS207G7/cs207-FinalProject/blob/master/backward_coeffs_formula.JPG" width="40%">
### 5. Reversible Reaction Rate
For reversible elementary reactions the rate of change follows the form:
<img src="https://github.com/CS207G7/cs207-FinalProject/blob/master/reversible_reaction_formula.JPG" width="40%">

Future Features
------------
### 1.Motivation and Feature Description

Our team of software developers expect to deliver a feature able to keep track of all the elementary reactions computed by a user.

The feature will efficiently browse into a list of reactions that have been computed and it will sort them by elements of interest such as species, temperature, date, and reversible or non-reversible reactions.

We think that the feature will be really useful for scientists interested in building their own database of elementary reactions. The devised feature will allow the user to explore reactions without the need for computing again. Beside saving time for the computation, the user might grow its own database that could be eventually shared with other users. 

Our feature will ultimately allow the user to find quickly the information related to the reactions already computed.

### 2.Feature and Code Base (and Package)

The feature is going to fit into our code base because it will store each reaction computed by chemkin. Our feature will store them in a database either adjacent to or combined with the NASA polynomials. Updates to our code will give the user methods enfolded in the module to find the reactions requested by the user.

### 3.Module

Our team is going to build a module  `history.py`. It will handle the results of each reactions computed by the user. It will store them into a sqlite3 database. The user will be able to access the information contained in the database thanks to the feature using the methods that follows.

### 4.Methods

A preliminary list of methods for selecting the reactions are listed below (parameters will be filled in at a later date):

**get_type()**
The method
```python
get_type()
```
is enabled by inputting the type(i.e. reversible or not reversible) of the reaction. This method returns the list of reactions of similar type.

**get_specie()**
The method
```python
get_specie()
```
is enabled by inputting species of the reaction (e.g. H, H2, O2, etc.). This method returns the list of reactions computed with the same species.

**get_temperature()**
The method
```python
get_temperature()
```
is enabled by inputting temperature of the reactions.This method returns the list of reactions computed with the same temperature.

**get_by_date()**
The method
```python
get_mass()
```
is enabled by inputting the mass for each specie in the reaction. This method returns the list of reactions computed with the same mass.


### 5.User's Experience

The user will be able to query any information contained in the reactions that have been computed. For instance, the user will be able to find all the reactions sort by elements of interest (e.g. type, species in the reactions, temperature of the reactions, etc).

### 6.External Dependencies

No additional external dependencies are anticipated to be required beyond what is used by our current version. Our new features will depend primarily on `sqlite3`.

''''
Coming Soon
''''
