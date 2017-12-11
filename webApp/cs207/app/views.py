from django.shortcuts import render, HttpResponse, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import time
import pymysql

def index(request):
    return render_to_response('app/main.html')

# def main(request):
# 	return render_to_response('app/main.html')

def docs(request):
	return render_to_response('app/docs.html')

@csrf_exempt
def filters(request):
	
	# species, T, reversible, non_reversible
	query = {}
	
	species, T, reversible, non_reversible = None, None, None, None 
	try:
		species = request.POST['species']
	except:
		pass
	
	try:
		T = request.POST['T']
	except:
		pass

	try: 
		reversible = request.POST['reversible']
	except:
		pass

	try:
		non_reversible = request.POST['non_reversible']
	except:
		pass


	if species:
		query['species'] = species.strip().split(',')
	else:
		query['species'] = None

	if T:
		query['temp'] = {'T':T, 'cmp': request.POST['comparator']}
	else:
		query['temp'] = None

	if reversible and not non_reversible:
		query['type'] = 'reversible'
	elif non_reversible and not reversible:
		query['type'] = 'non_reversible'
	else:
		query['type'] = 'both'

	### waiting for the result
	hr = HistoryReader()
	reaction_set_dict = hr.queryDatabase(query)

	if not reaction_set_dict:
		return render_to_response('app/main.html', {'data': [], 'empty': True})

	# turn dict into list
	data = []
	for _, val in reaction_set_dict.items():
		data.append( val )

	return render_to_response('app/main.html', {'data': data, 'empty': False})

# Create your models here.
class HistoryReader():
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
	            constraints.append('''A.reaction_set_id IN ({})'''.format(query_set))
	    
	    #Turn constraints into a query
	    for i, constraint in enumerate(constraints):
	        if i == 0:
	            query += " WHERE " + constraint
	        else:
	            query += " AND " + constraint
	    
	    query_sets = "SELECT * FROM reaction_set A" + query
	    query_reactions = "SELECT B.* FROM reaction_set A LEFT JOIN reaction B ON A.reaction_set_id = B.reaction_set_id" + query
	    
	    return query_sets, query_reactions

	def queryDatabase(self, dictionary):
	    query1, query2 = self.buildQueriesFromDict(dictionary)
	    cursor = self.getCursor()
	    cursor.execute(query1)
	    A = cursor.fetchall()
	    cursor.execute(query2)
	    B = cursor.fetchall()
	    res_dicts = {}

	    if not A or not B:
	    	return None

	    for reaction_set in A:

	    	rsid, origin, num_reaction, species, x, T, rrs, createAt = reaction_set

	    	res_dicts[rsid] = {	'rsid': rsid,
	    						'origin':origin, 
	    						'num_reaction': num_reaction,
	    						'species': species,
	    						'x': x,
	    						'T': T,
	    						'rrs': rrs,
	    						'createAt': createAt,
	    						'reactions':[]
	    					}

	    prev_rsid, current_total = list(res_dicts.keys())[0], 0
	    
	    for reaction in B:

	    	rid, rsid, rtype, reversible, equation, \
	    			coeff_params, V1, V2, createAt = reaction

	    	if rsid != prev_rsid:
	    		current_total += res_dicts[prev_rsid]['num_reaction']
	    	prev_rsid = rsid

	    	res_dicts[rsid]['reactions'].append({'rid':rid - current_total, 'rsid':rsid, 'rtype':rtype, \
	    			'reversible': bool(reversible), 'equation':equation, \
	    			'coeff_params':coeff_params, 'V1':V1, 'V2':V2, 'createAt':createAt})


	    return res_dicts
	


