import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import unittest
import pymysql

from kinetics.history import HistoryReader
#from history import HistoryReader


class test_Reaction_History(unittest.TestCase):
    
    #Are we able to connect
    def test_connection(self):
        # Create history reader
        hr = HistoryReader()
        # Make sure its connection is good
        self.assertTrue(hr.db.open)


    # Are we able to read data
    def test_query_history(self):
       hr = HistoryReader()
       queryDict = {'species': None, 'temp': None, 'type': None}
       #queryDict['species'] = ["H", "O"]
       queryDict['temp'] = {'T': 1600, 'cmp': '<'}
       #queryDict['type'] = 'non_reversible'
       result1, result2 = hr.queryDatabase(queryDict)
       #print(result1)
       self.assertFalse(result1 is None)
       self.assertFalse(result2 is None)

    # Check correct tables exist
    def test_database_tables(self):
        hr = HistoryReader()
        cursor = hr.getCursor()
        # Check whether reaction, reaction_set tables exist
        # might need to research SQL
        cursor.execute('''SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE="BASE TABLE" AND TABLE_SCHEMA ="cs207reactions"''')
        tableNames = cursor.fetchall()
        self.assertEqual(str(tableNames), "(('reaction',), ('reaction_set',))")
