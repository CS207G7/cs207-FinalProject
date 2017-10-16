import numpy as np
import xml.etree.ElementTree as ET

class inputReader:

	def __init__(self, input_path):
		try:
			tree = ET.parse(input_path)
		except ValueError as err:
			raise ValueError('Something went wrong with your XML file:\n' + str(err))
		self.root = tree.getroot()
		self.reactions = {}
		self.parse_reactions()


	def get_species(self):
		species = self.root.find('phase').find('speciesArray')
		species = species.text.strip().split(' ')
		print ('species:{}'.format(species))
		return species

	def parse_reactions(self):
		reactions = self.root.find('reactionData').findall('reaction')
		for i, reaction in enumerate(reactions):
			attributes = reaction.attrib
			reversible, rtype, rid = attributes['reversible'], attributes['type'], attributes['id']
			# Equation
			equation = reaction.find('equation').text
			# Arrhenius Params
			coeffs = reaction.find('rateCoeff').find('Arrhenius')
			A, E =  float(coeffs.find('A').text), float(coeffs.find('E').text)
			if coeffs.find('b'):
				arr_params = {'A': A, 'E': E, 'b': float(coeffs.find('b').text)}
			else:
				arr_params = {'A': A, 'E': E}

			# Concentration
			## TODO: probably need to deal with wrong input format
			reactants = reaction.find('rateCoeff').find('reactants').text.split(' ')
			products = reaction.find('rateCoeff').find('products').text.split(' ')
			# x = np.zeros( (len(reactants) + len(products), 1) )
			v1, v2 = np.zeros( ( len(reactants) + len(products), 1 ) ), np.zeros( ( len(reactants) + len(products), 1 ) )
			for i in range( len(reactants) ):
				# check format, e.g. H:1, not H:1O:2
				if reactants[i].count(':') is not 1:
					raise ValueError('check your reactants input format: ' + reactants)
				v1[i] = reactants[i].split(':')[1]
			for j in range( len(products) ):
				if products[j].count(':') is not 1:
					raise ValueError('check your products input format: ' + products)
				v2[i + j + 1] = products[j].split(':')[1]

			self.reactions[rid] = {
				'type': rtype,
				'reversible': reversible,
				'equation': equation,
				'species': self.get_species(),
				'coeff_params': arr_params,
				'v1': v1,
				'v2': v2
			}

class Reaction:

	class reaction_coeff:
		
		@classmethod
		def constant(self, k):
			"""Returns the constant reaction coeff
	    
		    INPUTS
		    =======
		    k: float, the constant reaction coeff
		    
		    RETURNS
		    ========
		    k: float, the constant reaction coeff
		    
		    EXAMPLES
		    =========
		    >>> const(1.0)
		    1.0
		    >>> const(3.773)
		    3.773
		    """
			return k

		@classmethod
		def arr(self, A, E, T, R=8.314):
			"""Returns the Arrhenius reaction rate coeff
		    
			INPUTS
		    =======
		    A: positive float, Arrhenius prefactor
		    E: float, activation energy for the reaction
		    T: float, temperature in Kelvin scale
		    
		    RETURNS
		    ========
		    coeff: float, the Arrhenius reaction coeff
		    
		    EXAMPLES
		    =========
		    >>> arr(10**7, 10**3, 10**2)
		    3003549.0889639612
		    """
		    # Check type for all args
			if type(A) is not int and type(A) is not float:
				raise TypeError("The Arrhenius prefactor A should be either int or float")
			if type(E) is not int and type(E) is not float:
				raise TypeError("Activation Energy should be either int or float")
			if type(T) is not int and type(T) is not float:
				raise TypeError("Temperature (in Kelvin scale) should be either int or float")
		    
			# Check under/over flow
			if A >= float('inf') or A <= float('-inf'):
				raise ValueError("The Arrhenius prefactor A is under/overflow")
			if E >= float('inf') or E <= float('-inf'):
				raise ValueError("Activation Energy E is under/overflow")
			if T >= float('inf') or T <= float('-inf'):
				raise ValueError("Temperature T is under/overflow")
		        
			# Check value requirements
			if A <= 0:
				raise ValueError("The Arrhenius prefactor A is strictly positive")
			if T < 0:
				raise ValueError("Temperature in Kelvin scale should be positive")
			return A * np.exp( - E / (R * T) )

		@classmethod
		def mod_arr(self, A, b, E, T, R=8.314):
			"""Returns the modified Arrhenius reaction rate coeff

			INPUTS
			=======
			A: positive float, Arrhenius prefactor
			b: real number, The modified Arrhenius parameter
			E: float, activation energy for the reaction
			T: float, temperature in Kelvin scale
			RETURNS
			========
			coeff: float, the Arrhenius reaction coeff
			
			EXAMPLES
			=========
			>>> mod_arr(10**7, 0.5, 10**3, 10**2)
			30035490.889639609
			"""
			# Check type for all args
			if type(A) is not int and type(A) is not float:
				raise TypeError("The Arrhenius prefactor A should be either int or float")
			if type(b) is not int and type(b) is not float:
				raise TypeError("The modified Arrhenius parameter b should be either int or float")
			if type(E) is not int and type(E) is not float:
				raise TypeError("Activation Energy E should be either int or float")
			if type(T) is not int and type(T) is not float:
				raise TypeError("Temperature (in Kelvin scale) T should be either int or float")

			# Check under/over flow
			if A >= float('inf') or A <= float('-inf'):
				raise ValueError("The Arrhenius prefactor A is under/overflow")
			if b >= float('inf') or b <= float('-inf'):
				raise ValueError("The modified Arrhenius parameter b is under/overflow")
			if E >= float('inf') or E <= float('-inf'):
				raise ValueError("Activation Energy E is under/overflow")
			if T >= float('inf') or T <= float('-inf'):
				raise ValueError("Temperature T is under/overflow")
				# Check value requirements
			if A <= 0:
				raise ValueError("The Arrhenius prefactor A is strictly positive")
			if T < 0:
				raise ValueError("Temperature in Kelvin scale should be positive")
			return A * (T**b) * np.exp( - E / (R * T) )

	@classmethod
	def reaction_rate(self, v1, v2, x, k):
		"""Returns the reaction rate for a system
		INPUTS
		=======
		v1: 2 x 3 float vector
		v2: 2 x 3 float vector
		x: 2 x 3 float vector, species concentrations
		k: 2 x 1 float/int list

		RETURNS
		========
		reaction rates: 1x3 float array, the reaction rate for each specie

		EXAMPLES
		=========
		>>> rr([[1,2,0],[0,0,2]], [[0,0,1],[1,2,0]], [1,2,1], [10,10])
		array([-30, -60,  20])
		"""
		try:
			x = np.array(x)
			v1 = np.array(v1)
			v2 = np.array(v2)
			k = np.array(k)
		except TypeError as err:
			raise TypeError("x and v should be either int or float vectors")
		if k.any() < 0:
			raise ValueError("reaction constant can't be negative")
		ws = k * np.prod(x ** v1, axis=1)
		rrs = np.sum((v2 - v1) * np.array([ws]).T, axis=0)
		return rrs