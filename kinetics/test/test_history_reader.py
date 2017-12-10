import unittest



class test_reaction_history(unittest.TestCase):
	#Are we able to connect
	def test_connection(self):
		#Create history reader
		#Make sure its connection is good (self.db.open)
		pass

	#Are we able to read data
	def test_query_history(self):
		pass

	#Check correct tables exist
	def test_database_tables(self):
		#Check whether reaction, reaction_set exist and have columns we expect
		#might need to research SQL
		pass


# def testDatabaseQuery():
# 	hr = HistoryReader()
# 	queryDict = {'species': None, 'temp': None, 'type': None}
# 	#queryDict['species'] = ["H", "O"]
# 	queryDict['temp'] = {'T': 1600, 'cmp': '<'}
# 	#queryDict['type'] = 'non_reversible'
# 	result1, result2 = hr.queryDatabase(queryDict)
# 	print(result1, result2)
