import sys
sys.path.append('src')

import chemkin

#Function: reaction_coeff_params
## testing for type errors 

def test_reaction_coeff_params_T_text():
    try:
        chemkin.Reaction.reaction_coeff_params(('panama'))
    except Exception as err:
        assert(type(err) == TypeError)

def test_reaction_coeff_params_T_negative():
    try:
        chemkin.Reaction.reaction_coeff_params(-10**2)
    except Exception as err:
        assert(type(err) == TypeError)

def test_reaction_coeff_params_T_flow():
    try:
        chemkin.Reaction.reaction_coeff_params(float('inf'))
    except Exception as err:
        assert(type(err) == TypeError)