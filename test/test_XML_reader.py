import sys
sys.path.append('../src')

import chemkin

def test_XML_reader_1():
	r_reader = chemkin.ReactionParser('xml/xml_good1.xml')
	expected = ['H', 'O', 'OH', 'H2', 'O2']
	assert r_reader.get_species() == expected, "ReactionParser getting incorrect species."

def test_XML_bad_reactants():
    r_reader = chemkin.ReactionParser('xml/xml_bad_reactants.xml')
    try:
        reactions = r_reader.parse_reactions()
    except Exception as err:
        assert type(err) == TypeError, "Bad reactants should raise a TypeError."

def test_XML_bad_products():
    r_reader = chemkin.ReactionParser('xml/xml_bad_products.xml')
    try:
        reactions = r_reader.parse_reactions()
    except Exception as err:
        assert type(err) == TypeError, "Bad products should raise a TypeError."

test_XML_reader_1()
test_XML_bad_reactants()
test_XML_bad_products()