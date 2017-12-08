import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#import sys
# sys.path.append('src')
import unittest
from kinetics import chemkin
import numpy as np

#Function: H_over_RT

# testing for correct values

reactions = chemkin.Reaction(chemkin.ReactionParser('kinetics/test/xml/xml_homework.xml'), T=3500)

class test_Backward_Reaction_Coeffs(unittest.TestCase):

	def test_H_over_RT_result(self):
	    H_O2 = np.array([[2.50000001, -2.30842973e-11, 1.61561948e-14, -4.73515235e-18, 4.98197357e-22, 25473.6599, -0.44668291], [3.28253784, 0.00148308754, -7.57966669e-07, 2.09470555e-10, -2.16717794e-14, -1088.45772, 5.4532312]]).T

	    Tmax = 3500.000
	    compare = np.array([3.69508857, 4.06676078, 5.08138715, 6.28213553, -2.93437561])
	    reactions.get_nasa_coeffs = H_O2
	    output = reactions.H_over_RT()
	    assert np.equal(output, compare).all() == 0, 'Expected outcome'


	def test_H_over_RT_bad_result(self):
	    H_O2 = np.array([[2.50000001, -2.30842973e-11, 1.61561948e-14, -4.73515235e-18, 4.98197357e-22, 25473.6599, -0.44668291], [3.28253784, 0.00148308754, -7.57966669e-07, 2.09470555e-10, -2.16717794e-14, -1088.45772, 5.4532312]]).T

	    Tmax = 3500.000
	    compare = np.array([3.59508857, 4.26676078, 5.98138715, 6.48213553, -2.73437561])
	    reactions.get_nasa_coeffs = H_O2
	    output = reactions.H_over_RT()
	    assert np.equal(output, compare).any() == False, 'Unexpected outcome'

	# testing for argument number


	def test_reaction_H_over_RT_argument_number(self):
	    try:
	        chemkin.Reaction.H_over_RT(10**4, 10**2, 10**7)
	    except TypeError as err:
	        assert type(err) == TypeError, 'Wrong args number'

	#Function: S_over_R

	# testing for correct values


	def test_S_over_R_result(self):
	    H_O2 = np.array([[2.50000001, -2.30842973e-11, 1.61561948e-14, -4.73515235e-18, 4.98197357e-22, 25473.6599, -0.44668291], [3.28253784, 0.00148308754, -7.57966669e-07, 2.09470555e-10, -2.16717794e-14, -1088.45772, 5.4532312]]).T

	    Tmax = 3500.000
	    compare = np.array([3.69508857, 4.06676078, 5.08138715, 6.28213553, -2.93437561])
	    reactions.get_nasa_coeffs = H_O2
	    output = reactions.S_over_R()
	    assert np.equal(output, compare).all() == 0, 'Expected outcome'


	def test_S_over_R_bad_result(self):
	    H_O2 = np.array([[2.50000001, -2.30842973e-11, 1.61561948e-14, -4.73515235e-18, 4.98197357e-22, 25473.6599, -0.44668291], [3.28253784, 0.00148308754, -7.57966669e-07, 2.09470555e-10, -2.16717794e-14, -1088.45772, 5.4532312]]).T

	    Tmax = 3500.000
	    compare = np.array([3.59508857, 4.26676078, 5.98138715, 6.48213553, -2.73437561])
	    reactions.get_nasa_coeffs = H_O2
	    output = reactions.S_over_R()
	    assert np.equal(output, compare).any() == False, 'Unexpected outcome'

	# testing for argument number


	def test_reaction_S_over_R_argument_number(self):
	    try:
	        chemkin.Reaction.S_over_R(10**4, 10**2, 10**7)
	    except TypeError as err:
	        assert type(err) == TypeError, 'Wrong args number'
