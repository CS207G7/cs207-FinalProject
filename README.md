# cs207-FinalProject
### This is the cs207 final project repo for group 7
[![Build Status](https://travis-ci.org/CS207G7/cs207-FinalProject.svg?branch=master)](https://travis-ci.org/CS207G7/cs207-FinalProject)
[![Coverage Status](https://coveralls.io/repos/github/CS207G7/cs207-FinalProject/badge.svg?branch=master)](https://coveralls.io/github/CS207G7/cs207-FinalProject?branch=master)

### `chemkin` -- Chemical Kinetics Computational toolkit
======

This `chemkin` is a collection of algorithms aimed at predicting the time evolution of species concentration, finding the rate of change of a chemical species and calculating the rate of change of a certain specie. For multiple irreversible elementary reactions the rate of change follows the form:

\begin{align}

  \sum_{i=1}^{N}{\nu_{ij}^{\prime}\mathcal{S}_{i}} \longrightarrow 
  \sum_{i=1}^{N}{\nu_{ij}^{\prime\prime}\mathcal{S}_{i}}, \qquad j = 1, \ldots, M

\end{align}

$$a=b$$

`chemkin` is designed for flexibility, portability, easiness of use and easiness of extension. Its software design follows an object-oriented approach and its code is written on Python.


Installation
------------

Download the package, and `from chemkin import *`, and you can access any function you wish.


Examples
------------
#### How to use

```python
parsed = ReactionParser('path_to_reaction_xml')
```
parse the XML and obtain the following reaction details:

1. species
2. basic information, such as reaction id, reaction type, reaction equations, and etc.
3. `v1` and `v2` for each reaction

```python
reactions = Reaction(parsed)
```
wrap the reactions information into a Reaction Class

```python
V1, V2 = reactions.reaction_components()
```
since there could be multiple reactions inside a given reaction set, 
we stack each `v1` into `V1`, and each `v2` to `V2`

```python
k = reactions.reaction_coeff_params(T)
```
since the coefficient type is implicity given in the XML file. If `Arrhenius` is found, we check if `b`
is given to decide using modified or regular arr; if `Constant` is found, we use constant coeff. 
we only need user to provide T of the current reaction set, and return the list of reaction coeffs.

```python
rr = ChemKin.reaction_rate(V1, V2, X, k)
```
The last thing we need user to provide is the `X`: concentration of species. With `V1`, `V2`, and `k` computed,
user can easily obtian reaction rate for each speicies.