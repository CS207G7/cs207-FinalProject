import sys
sys.path.append('src')

import chemkin

#Function: reaction_coeff_params
## testing for type errors 

def test_reaction_coeff_params_T_text():
    try:
        Reaction.reaction_coeff_params(('panama'))
    except TypeError as err:
        assert(type(err) == TypeError)

def test_reaction_coeff_params_T_negative():
    try:
        Reaction.reaction_coeff_params(-10**2)
    except ValueError as err:
        assert(type(err) == ValueError)

def test_reaction_coeff_params_T_flow():
    try:
        Reaction.reaction_coeff_params(float('inf'))
    except ValueError as err:
        assert(type(err) == ValueError)