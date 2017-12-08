import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from kinetics import chemkin

#Function: reaction_coeff_params
## testing for type errors 

class test_reaction_component_coefficients(unittest.TestCase):
    

    def test_reaction_coeff_params_T_text(self):
        try:
            # read src
            parsed = chemkin.ReactionParser('kinetics/test/xml/xml_homework.xml')
            reactions = chemkin.Reaction(parsed, 'panama')
        except Exception as err:
            assert(type(err) == TypeError)

    def test_reaction_coeff_params_T_negative(self):
        try:
            parsed = chemkin.ReactionParser('kinetics/test/xml/xml_homework.xml')
            reactions = chemkin.Reaction(parsed, -10**2)
        except Exception as err:
            assert(type(err) == ValueError)

    def test_reaction_coeff_params_T_flow(self):
        try:
            parsed = chemkin.ReactionParser('kinetics/test/xml/xml_homework.xml')
            reactions = chemkin.Reaction(parsed, float('inf'))
        except Exception as err:
            assert(type(err) == ValueError)