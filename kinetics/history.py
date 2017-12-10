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



class HistoryReader:
	def __init__(self):
		self.host="cs207reactions.cuj7kddh2nbn.us-east-1.rds.amazonaws.com"
		self.port=3306
		self.dbname="cs207reactions"
		self.user="rafettob"
		self.password="cs207g72017"
		self.db = pymysql.connect(self.host, user=self.user, port=self.port, passwd=self.password, db=self.dbname)

	def getCursor(self):
	    if not self.db.open:
	        self.db = pymysql.connect(host, user=user,port=port, passwd=password, db=dbname)
	    return self.db.cursor()

	# DEAL WITH SPACES
	def buildQueriesFromDict(self, dictionary):
	    query = ""
	    constraints = []
	    
	    #All given species must be included
	    species = dictionary['species']
	    if species != None:
	        if type(species) is not list:
	            species = [species]
	        for specie in list(species):
	            constraints.append('''species LIKE '%{}%\''''.format(specie))

	    #Temperature in given range
	    temp = dictionary['temp']
	    if temp is not None:
	        constraints.append('''T {} {}'''.format(temp['cmp'], temp['T']))
	    
	    #For reversibility, need to query the set of all reactions to find distinct
	    #reactions_sets with eligible reactions, and then use that as a subquery
	    reversible = dictionary['type']
	    if reversible is not None:
	        if reversible == 'reversible' or reversible == 'non_reversible':
	            query_set = '''SELECT DISTINCT reaction_set_id FROM reaction ''' + \
	                '''WHERE reversibility = {}'''.format(reversible == 'reversible')
	            constraints.append('''reaction_set_id IN ({})'''.format(query_set))
	    
	    #Turn constraints into a query
	    for i, constraint in enumerate(constraints):
	        if i == 0:
	            query += " WHERE " + constraint
	        else:
	            query += " AND " + constraint
	    
	    query_sets = "SELECT * FROM reaction_set" + query
	    query_reactions = "SELECT B.* FROM reaction_set A LEFT JOIN reaction B ON A.reaction_set_id = B.reaction_set_id" + query
	    
	    return query_sets, query_reactions

	def queryDatabase(self, dictionary):
	    query1, query2 = self.buildQueriesFromDict(dictionary)
	    cursor = self.getCursor()
	    cursor.execute(query1)
	    A = cursor.fetchall()
	    cursor.execute(query2)
	    B = cursor.fetchall()
	    return A, B

def testDatabaseQuery():
	hr = HistoryReader()
	queryDict = {'species': None, 'temp': None, 'type': None}
	#queryDict['species'] = ["H", "O"]
	queryDict['temp'] = {'T': 1600, 'cmp': '<'}
	#queryDict['type'] = 'non_reversible'
	result1, result2 = hr.queryDatabase(queryDict)
	print(result1, result2)

if __name__ == "__main__":
	testDatabaseQuery()
	