import uuid
import time
import sqlite3

class History:
	
	def __init__(self, filename, reactions_set, T, X, rr):
		self.filename = filename
		self.reactions = reactions_set.reactions
		self.species = reactions_set.species
		self.reaction_set_id = uuid.uuid4().hex
		self.T = T
		self.X = X
		self.rr = rr
		self.db = sqlite3.connect('data/history.sqlite')

	def write(self):
		self.put_to_db('reaction_set')
		self.process_reactions()
		print ('History Writer: your reactions {}\n have been cached successfully.'.format(str(self.reactions)))

	def process_reactions(self):

		for i, (_, reaction) in enumerate(self.reactions.items()):
			
			reaction_type = reaction['type']
			reversibility = reaction['reversible']
			equation = reaction['equation']
			coeff_params = reaction['coeff_params']
			v1, v2 = str(reaction['v1']), str(reaction['v2'])
			
			self.put_to_db('reaction', reaction_type=reaction_type, reversibility=reversibility, \
						   equation=equation, coeff_params=coeff_params, \
						  v1=v1, v2=v2, reaction_idx=i)
		return True

	def put_to_db(self, db_name, **kwargs):
	
		created_at = time.ctime(int(time.time()))
		cursor = self.db.cursor()
		
		if db_name == 'reaction_set':
			
			cursor.execute('''CREATE TABLE IF NOT EXISTS reaction_set (
			   reaction_set_id TEXT PRIMARY KEY NOT NULL,
			   filename TEXT NOT NULL,
			   num_reactions INTEGER NOT NULL,
			   species TEXT NOT NULL,
			   concentration TEXT NOT NULL,
			   T REAL NOT NULL,
			   reaction_rate TEXT NOT NULL,
			   createdAt TEXT NOT NULL)''')
			
			vals_to_insert = (self.reaction_set_id, self.filename, \
							  len(self.reactions), str(self.species), \
							  str(self.X), self.T,\
							  str(self.rr), created_at)
			
			cursor.execute('''INSERT INTO reaction_set (reaction_set_id, filename, num_reactions, 
						   species, concentration, T, reaction_rate, createdAt) 
						   VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', vals_to_insert)
		
		elif db_name == 'reaction':
			
			cursor.execute('''CREATE TABLE IF NOT EXISTS reaction (
			   reaction_id TEXT PRIMARY KEY NOT NULL,
			   reaction_set_id TEXT NOT NULL,
			   type TEXT NOT NULL, 
			   reversibility BIT NOT NULL, 
			   equation TEXT NOT NULL, 
			   coeff_params TEXT NOT NULL,
			   v1 TEXT NOT NULL,
			   v2 TEXT NOT NULL,
			   createdAt TEXT NOT NULL)''')
		
			reaction_idx, coeff_params, reaction_type, reversibility, equation, v1, v2 = \
				kwargs['reaction_idx'],kwargs['coeff_params'], kwargs['reaction_type'], \
				kwargs['reversibility'], kwargs['equation'], kwargs['v1'], kwargs['v2']
				
			reaction_id = self.reaction_set_id + '_' + str(reaction_idx)

			vals_to_insert = (reaction_id, self.reaction_set_id, reaction_type, reversibility, equation, 
							  str(coeff_params), v1, v2, created_at)
			cursor.execute('''INSERT INTO reaction (reaction_id, reaction_set_id, type, 
						   reversibility, equation, coeff_params, v1, v2, createdAt) 
						   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', vals_to_insert)
		self.db.commit()
		return True