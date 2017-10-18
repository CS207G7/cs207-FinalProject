import sys
#sys.path.append('../src')
sys.path.append('../src')
#sys.path.append('test')
#sys.path.append('test/xml')

import chemkin
import numpy as np

def test_XML_reader_1():
	r_reader = chemkin.ReactionParser('test/xml/xml_good1.xml')
	expected = ['H', 'O', 'OH', 'H2', 'O2']
	assert r_reader.get_species() == expected, "ReactionParser getting incorrect species."

def test_XML_bad_reactants():
    r_reader = chemkin.ReactionParser('test/xml/xml_bad_reactants.xml')
    try:
        reactions = r_reader.parse_reactions()
    except Exception as err:
        assert type(err) == ValueError, "Bad reactants should raise a TypeError."

def test_XML_bad_products():
    r_reader = chemkin.ReactionParser('test/xml/xml_bad_products.xml')
    try:
        reactions = r_reader.parse_reactions()
    except Exception as err:
        assert type(err) == ValueError, "Bad products should raise a TypeError."

def test_XML_reader_2_V1():
    r_reader = chemkin.ReactionParser('../test/xml/xml_good2.xml')# chemkin.ReactionParser('test/xml/xml_good2.xml')
    reactions = r_reader.parse_reactions()
    chem = chemkin.Reaction(r_reader)
    V1, V2 = chem.reaction_components()
    print(repr(chem))
    print(V1)
    assert all(V1 == [[1], [0], [0], [2], [1]]), "XML Reader loading incorrect v1 in file xml_good2.xml"

#def test_XML_reader_2_V2():
#    r_reader = chemkin.ReactionParser('test/xml/xml_good2.xml')
#    reactions = r_reader.parse_reactions()
#    chem = chemkin.Reaction(r_reader)
#    V1, V2 = chem.reaction_components()
#    assert all(V2 == [[0], [1], [1], [0], [0]]), "XML Reader loading incorrect v1 in file xml_good2.xml"

#Not yet implemented
def test_XML_homework():
    r_reader = chemkin.ReactionParser('test/xml/xml_homework.xml')
    reactions = r_reader.parse_reactions()

    chem = chemkin.Reaction(r_reader)
    T = 750
    X = [2, 1, 0.5, 1, 1]
    V1, V2 = chem.reaction_components()
    k = chem.reaction_coeff_params(T)
    rrs = chemkin.ChemKin.reaction_rate(V1, V2, X, k)
    ans = np.array([-3607077.87280406, -5613545.18362079, 9220623.05642485, 2006467.31081673,-2006467.31081673])
    assert (rrs - ans).all() < 0.000000001

#test_XML_reader_1()
#test_XML_bad_reactants()
#test_XML_bad_products()
# test_XML_homework()
test_XML_reader_2_V1()
#test_XML_reader_2_V2()

