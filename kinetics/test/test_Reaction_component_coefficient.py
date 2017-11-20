#import sys
#sys.path.append('src')

from kinetics import chemkin

#Function: reaction_coeff_params
## testing for type errors 

parsed = chemkin.ReactionParser('kinetics/test/xml/xml_homework.xml')

def test_reaction_coeff_params_T_text():
    try:
        # read src
        reactions = chemkin.Reaction(parsed, 'panama')
    except Exception as err:
        assert(type(err) == TypeError)

def test_reaction_coeff_params_T_negative():
    try:
        reactions = chemkin.Reaction(parsed, -10**2)
    except Exception as err:
        assert(type(err) == ValueError)

def test_reaction_coeff_params_T_flow():
    try:
        reactions = chemkin.Reaction(parsed, float('inf'))
    except Exception as err:
        assert(type(err) == ValueError)