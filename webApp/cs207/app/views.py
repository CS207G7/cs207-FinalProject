from django.shortcuts import render, HttpResponse, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

def index(request):
    return HttpResponse('Hello World!')

def main(request):
	return render_to_response('app/main.html')

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

	return render_to_response('app/main.html', {'data':[ {'id':1, 'reactions':'Learn Django 2.0 by building multiple web applications starting with Hello World and progressing to a robust blog app with user accounts.'},  \
		{'id':2, 'reactions': "I'm starting today a new tutorial series about the Django fundamentals. It's a complete beginner's guide to start learning Django. The material is divided in..."},\
		{'id':3, 'reactions':'Django Girls tutorial - the course material used for the DjangoGirls workshops · ​Learn Django - An entry level and project based course to learn Django · ​Intuitive 20 video tutorial series for Django beginners · ​Short beginner tutorial on building a basic blog site · ​Full Web Framework Python Django ...'}]})
	


	


