import numpy as np
import xml.etree.ElementTree as ET
from enum import Enum

class ReactionParser:

	def __init__(self, input_path):
		try:
			tree = ET.parse(input_path)
		except ValueError as err:
			raise ValueError('Something went wrong with your XML file:\n' + str(err))
		self.root = tree.getroot()

	def get_species(self):
		species = self.root.find('phase').find('speciesArray')
		species = species.text.strip().split(' ')
		print ('species:{}'.format(species))
		return species

	def parse_reactions(self):
		reaction_dict = {}
		reactions = self.root.find('reactionData').findall('reaction')
		
		for i, reaction in enumerate(reactions):
			attributes = reaction.attrib
			reversible, rtype, rid = attributes['reversible'], attributes['type'], attributes['id']
			# Equation
			equation = reaction.find('equation').text
			# Arrhenius Params
			const_coeff = reaction.find('rateCoeff').find('Constant')

			if const_coeff:
				coeff_params = {'k': const_coeff}
			else:
				coeffs = reaction.find('rateCoeff').find('Arrhenius')
				try:
					A, E =  float(coeffs.find('A').text), float(coeffs.find('E').text)
				except:
					raise ValueError('did not capture Arrhenius prefactor A and activation energy E, please re-check input format')
				
				if coeffs.find('b'):
					coeff_params = {'A': A, 'E': E, 'b': float(coeffs.find('b').text)}
				else:
					coeff_params = {'A': A, 'E': E}

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

			reaction_dict[rid] = {
				'type': rtype,
				'reversible': reversible,
				'equation': equation,
				'species': self.get_species(),
				'coeff_params': coeff_params,
				'v1': v1,
				'v2': v2
			}
			return reaction_dict


class ChemKin:

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
		def arr(self, **kwargs, T, R=8.314):
			"""Returns the Arrhenius reaction rate coeff
		    
			INPUTS
		    =======
		    kwargs:
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
		    A, E = kwargs['A'], kwargs['E']
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
		def mod_arr(self, **kwargs, T, R=8.314):
			"""Returns the modified Arrhenius reaction rate coeff

			INPUTS
			=======
			kwargs
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
			A, E, b = kwargs['A'], kwargs['E'], kwargs['b']
			
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
		k: 2 x 1 float/int list, coeffs

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

class Reaction:

	def __init__(self, reactions):
		self.reactions = reactions

	def __repr__(self):
		reaction_str = ''
		for reaction in self.reactions:
			reaction_str += (str(reaction) + '\n')

		return 'Reactions:\n---------------\n' + reaction_str

	def __len__(self):
		return len(self.reactions)

	def reaction_components(self):

		V1 = np.zeros((len(self.reactions, self.reactions['v1'].shape[1])))
		V2 = np.zeros((len(self.reactions, self.reactions['v2'].shape[1])))
		for i, reaction in enumerate(self.reactions):
			V1[i] = self.reactions['v1']
			V2[i] = self.reactions['v2']

		return V1, V2

	def reaction_coeff_params(self, T):
		
		coeffs = []
		for i, reaction in enumerate(self.reactions):
			if hasattr(reaction['coeff_params'], 'k'):
				# constant, T is ignored
				coeffs.append( ChemKin.reaction_rate.constant(reaction['coeff_params']['k']) )
			elif hasattr(reaction['coeff_params'], 'b'):
				# modified 
				coeffs.append( ChemKin.reaction_rate.mod_arr(reaction['coeff_params'], T) )
			else:
				coeffs.append( ChemKin.reaction_rate.arr(reaction['coeff_params'], T) )

		return coeffs
			

if __name__ == "__main__":

	T = 750
	X = [2, 1, 0.5, 1, 1]
	reactions = Reaction(ReactionParser('rxns.xml').parse_reactions())
	print (reactions)
	V1, V2 = reactions.reaction_components()
	k = reactions.reaction_coeff_params(T)
	print ( ChemKin.reaction_rate(V1, V2, X, k) )