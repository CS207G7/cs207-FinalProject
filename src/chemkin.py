import numpy as np
from src.nasa import getNASACoeff
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
			rtype, rid = attributes['type'], attributes['id']
			reversible = 1 if attributes['reversible'] == 'yes' else 0
			# Equation
			equation = reaction.find('equation').text
			# Arrhenius Params
			const_coeff = reaction.find('rateCoeff').find('Constant')

			if const_coeff is not None:
				k  = const_coeff.find('k')
				coeff_params = {'K': float(k.text)}
			else:

				coeffs = reaction.find('rateCoeff').find('Arrhenius')

				if coeffs is None:
					# modified Arrhenius
					coeffs = reaction.find('rateCoeff').find('modifiedArrhenius')
				
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
					raise ValueError('check your reactants input format: ' + str(reactants))
				v1[reactants[i].split(':')[0]] = reactants[i].split(':')[1]
			
			for j in range( len(products) ):
				if products[j].count(':') is not 1:
					raise ValueError('check your products input format: ' + str(products))
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
		>>> ChemKin.reaction_rate([[1,0],[2,0],[0,2]], [[0,1],[0,2],[1,0]], [1,2,1], [10,10])
		array([-30, -60,  20])
		"""
		try:
			x = np.array(x)
			v1 = np.array(v1).T
			v2 = np.array(v2).T
		except TypeError as err:
			raise TypeError("x and v should be either int or float vectors")
		
		if len(k) == 3:
			# contains backward
			coeffs, bw_coeffs, reversibles = k
			if coeffs.any() < 0 or bw_coeffs.any() < 0 :
				raise ValueError("reaction constant can't be negative")
		else:
			coeffs = np.array(k)
			if coeffs.any() < 0:
				raise ValueError("reaction constant can't be negative")

		fw_ws = coeffs * np.prod(x ** v1, axis=1)
		fw_rrs = np.sum((v2 - v1) * np.array([fw_ws]).T, axis=0)

		if len(k) == 3:
			bw_ws = bw_coeffs * np.prod(x ** v2, axis=1)
			bw_rrs = fw_rrs - (np.sum((v2 - v1) * np.array([bw_ws]).T, axis=0))
			rrs = []
			for i, reversible in enumerate(reversibles):
				if reversible:
					rrs += [ bw_rrs[i].tolist() ]
				else:
					rrs += [ fw_rrs[i].tolist() ]
			return rrs
		else:
			return fw_rrs

class Reaction:

	def __init__(self, parser, T=750):
		self.species = parser.get_species()
		self.reactions = parser.parse_reactions()
		self.V1, self.V2  = self.reaction_components()
		self.p0 = 1.0e+05 # Pa
		self.R = 8.3144598 # J / mol / K

		if type(T) is not int and type(T) is not float:
				raise TypeError("Temperature (in Kelvin scale) should be either int or float")
		elif T < 0:
				raise ValueError("Temperature T should be postiive")
		elif T >= float('inf') or T <= float('-inf'):
				raise ValueError("Temperature T is under/overflow")
		else:
			self.T = T

		self.gamma = np.sum(self.V2 - self.V1, axis=0)
		self.get_nasa_coeffs()

	def __repr__(self):
		reaction_str = ''
		for rid, reaction in self.reactions.items():
			reaction_str += (rid + '\n' + str(reaction) + '\n')

		return 'Reactions:\n---------------\n' + reaction_str

	def __len__(self):
		return len(self.reactions)

	'''
		functions for computing reversible reaction
	'''

	def get_nasa_coeffs(self):
		""" Return the NASA polynomial coeffs for each species
		INPUTS
		=======
		self

		RETURNS
		========
		nasa_coeffs: a list, where nasa_coeffs[i] is the NASA coeffs for the ith species"""
		self.nasa_coeffs = np.zeros((len(self.species), 7))
		for i, specie in enumerate(self.species):
			self.nasa_coeffs[i] = getNASACoeff(specie, self.T)

	def H_over_RT(self):
		""" Return H over RT, Enthalpy
		INPUTS
		=======
		self

		RETURNS
		========
		H_RT: a list, where H_RT[i] is the enthalpy for the ith species"""
		a = self.nasa_coeffs
		H_RT = (a[:,0] + a[:,1] * self.T / 2.0 + a[:,2] * self.T**2.0 / 3.0 
				+ a[:,3] * self.T**3.0 / 4.0 + a[:,4] * self.T**4.0 / 5.0 
				+ a[:,5] / self.T)

		return H_RT

	def S_over_R(self):
		""" Return S over R, Entropy
		INPUTS
		=======
		self

		RETURNS
		========
		S_R: a list, where S_R[i] is the entropy for the ith species"""
		a = self.nasa_coeffs
		S_R = (a[:,0] * np.log(self.T) + a[:,1] * self.T + a[:,2] * self.T**2.0 / 2.0 
			+ a[:,3] * self.T**3.0 / 3.0 + a[:,4] * self.T**4.0 / 4.0 + a[:,6])
		return S_R

	def backward_coeffs(self, kf):

		""" Return backward reation coeffs for each reactions
		INPUTS
		=======
		kf: the forward reaction coeffs

		RETURNS
		========
		coeffs: a list, where coeffs[i] is the reaction coeffs for the i_th reaction"""

		# Change in enthalpy and entropy for each reaction

		h_over_rt = self.H_over_RT()
		s_over_r = self.S_over_R()

		delta_H_over_RT = np.matmul(h_over_rt.reshape(1, len(h_over_rt)), self.V2 - self.V1)
		delta_S_over_R = np.matmul(s_over_r.reshape(1, len(s_over_r)), self.V2 - self.V1)


		# Negative of change in Gibbs free energy for each reaction 
		delta_G_over_RT = delta_S_over_R - delta_H_over_RT

		# Prefactor in Ke
		fact = self.p0 / self.R / self.T
		# Ke
		ke = fact**self.gamma * np.exp(delta_G_over_RT)

		return kf / ke

	'''
		Functions 
	'''

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

	def reaction_coeff_params(self):
		""" Return reation coeffs for each reactions
		INPUTS
		=======
		self

		RETURNS
		========
		coeffs: a list, where coeffs[i] is the reaction coefficient for the i_th reaction
		"""
		coeffs = []
		reversibles = []

		for _, reaction in self.reactions.items():
			
			if 'K' in reaction['coeff_params']:
				# constant, T is ignored
				coeffs.append( ChemKin.reaction_coeff.constant(reaction['coeff_params']['K']) )
			elif 'b' in reaction['coeff_params']:
				# modified 
				coeffs.append( ChemKin.reaction_coeff.mod_arr(self.T, A=reaction['coeff_params']['A'], \
					b=reaction['coeff_params']['b'], E=reaction['coeff_params']['E'] ) )
			else:
				coeffs.append( ChemKin.reaction_coeff.arr(self.T, A=reaction['coeff_params']['A'], \
					E=reaction['coeff_params']['E'] ) )

			reversibles += [ reaction['reversible'] ]

		if np.sum(reversibles) == 0:
			return np.array(coeffs)
		else:
			return np.array(coeffs), self.backward_coeffs(coeffs), reversibles

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
	# T = 750
	# X = [2, 1, 0.5, 1, 1] #,1, 1, 1]
	# reactions = Reaction(ReactionParser('../test/xml/xml_homework.xml'), T)
	# V1, V2 = reactions.reaction_components()
	# k = reactions.reaction_coeff_params()
	# print (reactions.species )
	# print ( ChemKin.reaction_rate(V1, V2, X, k) )
	# reactions = Reaction(ReactionParser('../data/rxns_reversible.xml'), T)
	# V1, V2 = reactions.reaction_components()
	# k = reactions.reaction_coeff_params()
	# print ( ChemKin.reaction_rate(V1, V2, X, k) )