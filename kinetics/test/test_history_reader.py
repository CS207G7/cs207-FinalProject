import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import pymysql
from history import HistoryReader


class test_reaction_history(unittest.TestCase):

    # Are we able to connect
    def test_connection(self):
        # Create history reader
        hr = history.HistoryReader()
        # Make sure its connection is good (self.db.open)

        connection = {'host': "cs207reactions.cuj7kddh2nbn.us-east-1.rds.amazonaws.com",
                      'port': 3306, 'dbname': "cs207reactions", 'user': "rafettob", 'password': "cs207g72017"}

        pass:

        except Exception as err:

        assert type(err) == ValueError, 'Bad connection'

    # Are we able to read data
    def test_query_history(self):
        pass

    # Check correct tables exist
    def test_database_tables(self):
        # Check whether reaction, reaction_set exist and have columns we expect
        # might need to research SQL
        pass


# def testDatabaseQuery():
# 	hr = HistoryReader()
# 	queryDict = {'species': None, 'temp': None, 'type': None}
# 	#queryDict['species'] = ["H", "O"]
# 	queryDict['temp'] = {'T': 1600, 'cmp': '<'}
# 	#queryDict['type'] = 'non_reversible'
# 	result1, result2 = hr.queryDatabase(queryDict)
# 	print(result1, result2)
