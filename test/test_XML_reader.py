import sys
sys.path.append('../src')

import chemkin

def test_XML_bad_reactants():
	raise NotImplementedError()

def test_XML_bad_products():
	raise NotImplementedError()

def test_XML_reader_1():
	r_reader = chemkin.ReactionParser('xml/xml_good1.xml')
	#print(r_reader)
	expected = ['H', 'O', 'OH', 'H2', 'O2']
	assert r_reader.get_species() == expected, "ReactionParser getting incorrect species."

test_XML_reader_1()

#test_XML_bad_reactants()
#test_XML_bad_products()