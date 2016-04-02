import json
import urllib.request
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.core import serializers
# Create your views here.

def search_flipkart(request):
	equest = urllib.request.Request("https://affiliate-api.flipkart.net/affiliate/search/json?query=adidas+golf+shoes&resultCount=5")
	equest.add_header('Fk-Affiliate-Id', 'manavbhar')
	equest.add_header('Fk-Affiliate-Token','55b95905e3734978bc1aa18df555248a')
	contents = urllib.request.urlopen(equest).read().decode("utf-8")
	#return HttpResponse(html)
	return JsonResponse(contents,safe=False)

def get_text(request):
	print(request)
	contents1 = {"name":"djaslkd"}
	return JsonResponse(contents1,safe=False)	

	