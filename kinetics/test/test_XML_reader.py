#import sys
#sys.path.append('../src')
#sys.path.append('src')
#sys.path.append('test')
#sys.path.append('test/xml')
import unittest
from kinetics import chemkin
import numpy as np

class test_XML_Readers(unittest.TestCase):

	def test_XML_reader_1(self):
		r_reader = chemkin.ReactionParser('kinetics/test/xml/xml_good1.xml')
		expected = ['H', 'O', 'OH', 'H2', 'O2']
		assert r_reader.get_species() == expected, "ReactionParser getting incorrect species."

	def test_XML_bad_reactants(self):
	    r_reader = chemkin.ReactionParser('kinetics/test/xml/xml_bad_reactants.xml')
	    try:
	        reactions = r_reader.parse_reactions()
	    except Exception as err:
	        assert type(err) == ValueError, "Bad reactants should raise a TypeError."

	def test_XML_bad_products(self):
	    r_reader = chemkin.ReactionParser('kinetics/test/xml/xml_bad_products.xml')
	    try:
	        reactions = r_reader.parse_reactions()
	    except Exception as err:
	        assert type(err) == ValueError, "Bad products should raise a TypeError."

	def test_XML_reader_2_V1(self):
	    r_reader = chemkin.ReactionParser('kinetics/test/xml/xml_good2.xml')# chemkin.ReactionParser('test/xml/xml_good2.xml')
	    reactions = r_reader.parse_reactions()
	    chem = chemkin.Reaction(r_reader, 750)
	    V1, V2 = chem.reaction_components()
	    print(repr(chem))
	    print(V1)
	    assert all(V1 == [[1], [0], [0], [2], [1]]), "XML Reader loading incorrect v1 in file xml_good2.xml"

	def test_XML_reader_2_V2(self):
	   r_reader = chemkin.ReactionParser('kinetics/test/xml/xml_good2.xml')
	   reactions = r_reader.parse_reactions()
	   chem = chemkin.Reaction(r_reader, 750)
	   V1, V2 = chem.reaction_components()
	   assert all(V2 == [[0], [1], [1], [0], [0]]), "XML Reader loading incorrect v1 in file xml_good2.xml"

	def test_XML_homework(self):
	    r_reader = chemkin.ReactionParser('kinetics/test/xml/xml_homework.xml')
	    reactions = r_reader.parse_reactions()
	    T = 750
	    chem = chemkin.Reaction(r_reader, T)
	    X = [2, 1, 0.5, 1, 1]
	    V1, V2 = chem.reaction_components()
	    k = chem.reaction_coeff_params()
	    rrs = chemkin.ChemKin.reaction_rate(V1, V2, X, k)
	    ans = np.array([-3607077.87280406, -5613545.18362079, 9220623.05642485, 2006467.31081673,-2006467.31081673])
	    diffs = np.array([rrs - ans])
	    #print(diffs)
	    assert (diffs < 0.0000001).all()

	def test_XML_reversible(self):
	    r_reader = chemkin.ReactionParser('kinetics/test/xml/rxns_reversible.xml')
	    reactions = r_reader.parse_reactions()
	    chem = chemkin.Reaction(r_reader, 1500)
	    X = [2, 1, 0.5, 1, 1, 1., 0.5, 1.5]
	    V1, V2 = chem.reaction_components()
	    k = chem.reaction_coeff_params()
	    rrs = chemkin.ChemKin.reaction_rate(V1, V2, X, k)
	    ans = np.array([89270713727987.25, -320691804865713.7, -112277955225117.38, 86184567576824.7, 82059197481207.2, 336486898686318.2, -8582946144078.839, -152448671237427.4])
	    diffs = np.array([rrs - ans])
	    #print(diffs)
	    assert (diffs < 0.0000001).all()

	#def test_XML_reversible_and_irreversible():
	#    r_reader = chemkin.ReactionParser('kinetics/test/xml/reversible_and_irreversible.xml')
	#    reactions = r_reader.parse_reactions()
	#    chem = chemkin.Reaction(r_reader, 1500)
	#    X = [2, 1, 0.5, 1, 1, 1., 0.5, 1.5]
	#    V1, V2 = chem.reaction_components()
	#    k = chem.reaction_coeff_params()
	#    rrs = chemkin.ChemKin.reaction_rate(V1, V2, X, k)
	#    ans = np.array([89270713727987.25, -320691804865713.7, -112277955225117.38, 86184567576824.7, 82059197481207.2, 336486898686318.2, -8582946144078.839, -152448671237427.4])
    

#test_XML_reader_1()
#test_XML_bad_reactants()
#test_XML_bad_products()
#test_XML_homework()
#test_XML_reader_2_V1()
#test_XML_reader_2_V2()
#test_XML_reversible()