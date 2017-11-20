#import sys
#sys.path.append('src')
import unittest
from kinetics import nasa

class test_NASA_Coeff(unittest.TestCase):

	#Test code works for a given molecule at a given temperature in the low range
	def test_NASA_coefficients(self):
		coeff = nasa.getNASACoeff("H", 300)
		self.assertEqual(coeff, [2.5, 7.05332819e-13, -1.99591964e-15, 2.30081632e-18, -9.27732332e-22, 25473.6599, -0.446682853])

	#Test code works for a given molecule at a given temperature in the high range
	def test_NASA_coefficients_2(self):
		coeff = nasa.getNASACoeff("H2O", 1500)
		self.assertEqual(coeff, [3.03399249, 0.00217691804, -1.64072518e-07, -9.7041987e-11, 1.68200992e-14, -30004.2971, 4.9667701])

	#Test code breaks for temperatures below range
	def test_NASA_coefficients_LowTemp(self):
		self.assertRaises(Exception, nasa.getNASACoeff, "H", 199)

	#Test code breaks for temperatures above range
	def test_NASA_coefficients_HighTemp(self):
		self.assertRaises(Exception, nasa.getNASACoeff, "OH", 3501)

	#Test code breaks for unknown species
	def test_NASA_coefficients_UnknownSpecies(self):
		self.assertRaises(Exception, nasa.getNASACoeff, "Ag", 1100)