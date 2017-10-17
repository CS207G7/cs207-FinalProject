import numpy as np
import xml.etree.ElementTree as ET

class ReactionParser:

	def __init__(self, input_path):
		try:
			tree = ET.parse(input_path)
		except ValueError as err:
			raise ValueError('Something went wrong with your XML file:\n' + str(err))
		self.root = tree.getroot()

	def get_species(self):
		""" Returns the species list of the current reaction
	    
		    INPUTS
		    =======
		    self
		    
		    RETURNS
		    ========
		    species: list of string
		"""
		species = self.root.find('phase').find('speciesArray')
		species = species.text.strip().split(' ')
		return species

	def parse_reactions(self):

		""" Parse the reactions from XML, and returns the reaction dictionary
	    
		    INPUTS
		    =======
		    self
		    
		    RETURNS
		    ========
		    reaction_dict: a dictionary, where key is the reaction id, val is the reaction details
		    
		"""
		reaction_dict = {}
		reactions = self.root.find('reactionData').findall('reaction')
		
		for i, reaction in enumerate(reactions):
			attributes = reaction.attrib
			reversible, rtype, rid = attributes['reversible'], attributes['type'], attributes['id']
			# Equation
			equation = reaction.find('equation').text
			# Arrhenius Params
			const_coeff = reaction.find('rateCoeff').find('Constant')

			if const_coeff is not None:
				coeff_params = {'k': const_coeff}
			else:
				coeffs = reaction.find('rateCoeff').find('Arrhenius')
				try:
					A, E =  float(coeffs.find('A').text), float(coeffs.find('E').text)
				except:
					raise ValueError('did not capture Arrhenius prefactor A and activation energy E, please re-check input format')
				
				if coeffs.find('b') is not None:
					coeff_params = {'A': A, 'E': E, 'b': float(coeffs.find('b').text)}
				else:
					coeff_params = {'A': A, 'E': E}

			reactants = reaction.find('reactants').text.split(' ')
			products = reaction.find('products').text.split(' ')
			# x = np.zeros( (len(reactants) + len(products), 1) )
			#v1, v2 = np.zeros( ( len(reactants) + len(products), 1 ) ), np.zeros( ( len(reactants) + len(products), 1 ) )
			v1, v2 = {}, {}
			for specie in self.get_species():
				v1[specie], v2[specie] = 0, 0
			
			for i in range( len(reactants) ):
				# check format, e.g. H:1, not H:1O:2
				if reactants[i].count(':') is not 1:
					raise ValueError('check your reactants input format: ' + reactants)
				v1[reactants[i].split(':')[0]] = reactants[i].split(':')[1]
			
			for j in range( len(products) ):
				if products[j].count(':') is not 1:
					raise ValueError('check your products input format: ' + products)
				v2[products[j].split(':')[0]] = products[j].split(':')[1]

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
		    >>> ChemKin.reaction_coeff.constant(1.0)
		    1.0
		    >>> ChemKin.reaction_coeff.constant(3.773)
		    3.773
		    """
			return k

		@classmethod
		def arr(self, T, R=8.314, **kwargs):
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
		    >>> ChemKin.reaction_coeff.arr(10**2, A=10**7, E=10**3)
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
		def mod_arr(self, T, R=8.314, **kwargs):
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
			>>> ChemKin.reaction_coeff.mod_arr(10**2, A=10**7, b=0.5, E=10**3)
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
		v1: float vector
		v2: float vector
		x: float vector, species concentrations
		k: float/int list, reaction coeffs

		RETURNS
		========
		reaction rates: 1x3 float array, the reaction rate for each specie

		EXAMPLES
		=========
		>>> ChemKin.reaction_rate([[1,2,0],[0,0,2]], [[0,0,1],[1,2,0]], [1,2,1], [10,10])
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

	def __init__(self, parser):
		self.species = parser.get_species()
		self.reactions = parser.parse_reactions()

	def __repr__(self):
		reaction_str = ''
		for rid, reaction in self.reactions.items():
			reaction_str += (rid + '\n' + str(reaction) + '\n')

		return 'Reactions:\n---------------\n' + reaction_str

	def __len__(self):
		return len(self.reactions)

	def reaction_components(self):
		""" Return the V1 and V2 of the reactions
		INPUTS
		=======
		self

		RETURNS
		========
		V1: a numpy array, shows each specie's coeff in formula in the forward reaction
		V2: a numpy array, shows each specie's coeff in formula in the backward reaction
		"""
		V1 = np.zeros((len(self.species), len(self.reactions)))
		V2 = np.zeros((len(self.species), len(self.reactions)))
		
		for i, (_, reaction) in enumerate(self.reactions.items()):
			V1[:,i] = [val for _, val in reaction['v1'].items()]
			V2[:,i] = [val for _, val in reaction['v2'].items()]

		return V1, V2

	def reaction_coeff_params(self, T):
		""" Return reation coeffs for each reactions
		INPUTS
		=======
		self
		T: float, the temperature of reaction

		RETURNS
		========
		coeffs: a list, where coeffs[i] is the reaction coefficient for the i_th reaction
		"""
		coeffs = []
		for i, reaction in enumerate(self.reactions):
			if hasattr(reaction['coeff_params'], 'k'):
				# constant, T is ignored
				coeffs.append( ChemKin.reaction_rate.constant(reaction['coeff_params']['k']) )
			elif hasattr(reaction['coeff_params'], 'b'):
				# modified 
				coeffs.append( ChemKin.reaction_rate.mod_arr(T, A=reaction['coeff_params']['A'], \
					b=reaction['coeff_params']['b'], E=reaction['coeff_params']['E'] ) )
			else:
				coeffs.append( ChemKin.reaction_rate.arr(T, A=reaction['coeff_params']['A'], \
					E=reaction['coeff_params']['E'] ) )

		return coeffs
			

if __name__ == "__main__":

	"""
	parsed = ReactionParser('path_to_reaction_xml')
	-------------------------
	parse the XML and obtain reaction details:

	1. species
	2. basic information, such as reaction id, reaction type, reaction equations, and etc.
	3. v1 and v2 for each reaction
	
	reactions = Reaction(parsed)
	-------------------------
	wrap the reactions information into a Reaction Class

	V1, V2 = reactions.reaction_components()
	-------------------------
	since there could be multiple reactions inside a given reaction set, 
	we stack each v1 into V1, and each v2 to V2
	
	k = reactions.reaction_coeff_params(T)
	-------------------------
	since the coefficient type is implicity given in the XML file. If <Arrhenius> is found, we check if 'b'
	is given to decide using modified or regular arr; if <Constant> is found, we use constant coeff. 
	we only need user to provide T of the current reaction set, and return the list of reaction coeffs.
	
	rr = ChemKin.reaction_rate(V1, V2, X, k)
	-------------------------
	The last thing we need user to provide is the X: concentration of species. With V1, V2, and k computed,
	user can easily obtian reaction rate for each speicies.
	"""
	T = 750
	X = [2, 1, 0.5, 1, 1]
	reactions = Reaction(ReactionParser('rxns.xml'))
	V1, V2 = reactions.reaction_components()
	k = reactions.reaction_coeff_params(T)
	print (reactions.species )
	print ( ChemKin.reaction_rate(V1, V2, X, k) )