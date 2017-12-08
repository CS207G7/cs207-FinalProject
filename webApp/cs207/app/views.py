from django.shortcuts import render, HttpResponse, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

def index(request):
    return HttpResponse('Hello World!')

def main(request):
	return render_to_response('app/main.html')

@csrf_exempt
def filters(request):
	
	button_title = '...'
	render(request, 'app/main.html', {'button_title':button_title})
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
	return render(request, 'app/main.html')#render_to_response('app/main.html')
	


	


