import json
import urllib.request
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from .models  import ProductInformation
# Create your views here.

def search_flipkart(request):
	equest = urllib.request.Request("https://affiliate-api.flipkart.net/affiliate/search/json?query=adidas+golf+shoes&resultCount=5")
	equest.add_header('Fk-Affiliate-Id', 'manavbhar')
	equest.add_header('Fk-Affiliate-Token','55b95905e3734978bc1aa18df555248a')
	contents = urllib.request.urlopen(equest).read().decode("utf-8")
	#return HttpResponse(html)
	return JsonResponse(contents,safe=False)


@csrf_exempt
def get_text(request):
	print(request)
	print(request.META)
	if request.method == 'POST':
		print(request.body)
	contents1 = {"name":"Yolo so"}
	return JsonResponse(contents1, safe=False)


@csrf_exempt
def get_results(request):
	products = ProductInformation.objects.filter(pk__gt=10).values_list('id', 'name', 'referredFrom', 'price', 'listPrice', 'imageLink')[:10]
	return_dict = {}
	for i in range(len(products.values())):
		return_dict[str(i+1)] = products.values()[i]
	#products_list = json.dumps(list(products), cls=DjangoJSONEncoder)
	#products_json = json.loads(products_list)
	return JsonResponse(products_json, safe=False)