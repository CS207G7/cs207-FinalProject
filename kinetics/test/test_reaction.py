import sys
import numpy as np
#sys.path.append('../src')
#sys.path.append('src')
#sys.path.append('test')
#sys.path.append('test/xml')
import unittest
from kinetics import chemkin

class test_reactions(unittest.TestCase):

	def test_reaction_result(self):
	    V1, V2 = np.array([[1,2,3],[2,1,2]]).T, np.array([[1,1,2],[5,1,1]]).T
	    X = [1,2,1]
	    k = [6,6]
	    compare = np.array([36, -24, -36])
	    output = chemkin.ChemKin.reaction_rate(V1, V2, X, k)
	    assert np.equal(output, compare).all() == 1, 'Unexpected outcome'

	def test_reaction_type_error(self):
	    V1, V2 = np.array([[1,2,'lol'],[2,1,2]]).T, np.array([[1,'test',2],[5,1,1]]).T
	    X = [1,2,1]
	    k = [6,6]
	    try:
	        chemkin.ChemKin.reaction_rate(V1, V2, X, k)
	    except Exception as err:
	        assert type(err) == TypeError, 'Bad args format'

	def test_reaction_coeff_pos(self):
	    V1, V2 = np.array([[1,2,3],[2,1,2]]).T, np.array([[1,1,2],[5,1,1]]).T
	    X = [1,2,1]
	    k = [6, -6]
	    try:
	        chemkin.ChemKin.reaction_rate(V1, V2, X, k)
	    except Exception as err:
	        assert type(err) == ValueError, 'Bad k'

# test_reaction_result()
# test_reaction_type_error()
# test_reaction_coeff_pos()