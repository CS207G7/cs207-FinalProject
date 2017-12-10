import time
import pymysql	

class History:
	
	def __init__(self, filename, reactions_set, T, X, rr):
		self.filename = filename
		self.reactions = reactions_set.reactions
		self.species = reactions_set.species
		self.T = T
		self.X = X
		self.rr = rr

		#Initialize connection details for remote database
		self.host="cs207reactions.cuj7kddh2nbn.us-east-1.rds.amazonaws.com"
		self.port=3306
		self.dbname="cs207reactions"
		self.user="rafettob"
		self.password="cs207g72017"
		self.db = pymysql.connect(self.host, user=self.user, port=self.port, passwd=self.password, db=self.dbname)


	def write(self):
		cursor = self.db.cursor()
		created_at = time.strftime('%Y-%m-%d %H:%M:%S')
		self.reaction_set_id = self.write_reaction_set(cursor, created_at)
		#print("Reaction Set ID: ", self.reaction_set_id)
		self.process_reactions(cursor, created_at, self.reaction_set_id)
		#print ('History Writer: your reactions {}\n have been cached successfully.'.format(str(self.reactions)))

	def process_reactions(self, cursor, timestamp, reaction_set_id):
		for i, (_, reaction) in enumerate(self.reactions.items()):
			reaction_type = reaction['type']
			reversibility = reaction['reversible']
			equation = reaction['equation']
			coeff_params = reaction['coeff_params']
			v1, v2 = str(reaction['v1']), str(reaction['v2'])
			
			self.write_reaction(cursor, timestamp, reaction_set_id, reaction_type=reaction_type, reversibility=reversibility, \
						   equation=equation, coeff_params=coeff_params, \
						  v1=v1, v2=v2)

	def write_reaction_set(self, cursor, timestamp):
		#Write each reaction_set to the database
		cursor.execute('''CREATE TABLE IF NOT EXISTS reaction_set (
		    reaction_set_id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
		    filename INT NOT NULL,
		    num_reactions INTEGER NOT NULL,
		    species TEXT NOT NULL,
		    concentration TEXT NOT NULL,
		    T REAL NOT NULL,
		    reaction_rate TEXT NOT NULL,
		    createdAt DATETIME NOT NULL)''')
		
		vals_to_insert = (self.filename, len(self.reactions), str(self.species), \
						  str(self.X), self.T, str(self.rr), timestamp)
		
		cursor.execute('''INSERT INTO reaction_set (filename, num_reactions, 
					   species, concentration, T, reaction_rate, createdAt) 
					   VALUES (%s, %s, %s, %s, %s, %s, %s)''', vals_to_insert)

		self.db.commit()
		return cursor.lastrowid

	def write_reaction(self, cursor, timestamp, reaction_set_id, **kwargs):
		#Write each reaction to the database
		cursor.execute('''CREATE TABLE IF NOT EXISTS reaction (
		    reaction_id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
		    reaction_set_id INTEGER NOT NULL,
		    type TEXT NOT NULL, 
		    reversibility BIT NOT NULL, 
		    equation TEXT NOT NULL, 
		    coeff_params TEXT NOT NULL,
		    v1 TEXT NOT NULL,
		    v2 TEXT NOT NULL,
		    createdAt DATETIME NOT NULL)''')
	
		coeff_params, reaction_type, reversibility, equation, v1, v2 = \
			kwargs['coeff_params'], kwargs['reaction_type'], \
			kwargs['reversibility'], kwargs['equation'], kwargs['v1'], kwargs['v2']

		vals_to_insert = (reaction_set_id, reaction_type, reversibility, equation, 
						  str(coeff_params), v1, v2, timestamp)
		cursor.execute('''INSERT INTO reaction (reaction_set_id, type, 
					   reversibility, equation, coeff_params, v1, v2, createdAt) 
					   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', vals_to_insert)
		self.db.commit()