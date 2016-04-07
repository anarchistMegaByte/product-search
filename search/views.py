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
	#print(request)
	#print(request.META)
	#print(type(request.body.decode('utf-8')))
	text = request.body.decode('utf-8')
	t_j = json.loads(text)
	print(t_j['string'].replace('\n', ' '))
	#if request.method == 'POST':
		#print(request.body)
	contents1 = {"name":"Yolo so"	}
	return JsonResponse(contents1, safe=False)


@csrf_exempt
def get_results(request):
	products = ProductInformation.objects.filter(pk__gt=10)[:10]
	
	return_dict = {}
	for i in range(len(products.values())):
		return_dict[i+1] = { 'id'               : products[i].id               ,
		                     'name'             : products[i].name             ,
		                     'referredFrom'     : products[i].referredFrom     ,
		                     'price'            : products[i].price            ,
		                     'listPrice'        : products[i].listPrice        ,
		                     'imageLink'        : products[i].imageLink        } 
	#products_list = json.dumps(list(products), cls=DjangoJSONEncoder)
	#products_json = json.loads(products_list)
	return JsonResponse(return_dict, safe=False)

def algorithm(brand, cat, sub):
	is_brand_present = False
	is_category_present = False
	is_subCategory_present = False
	brand_id = []
	category_id = []
	subCategory_id = []
	items_b = ProductInformation.objects.filter(brand__icontains=brand)
	if items_b.count() > 0 :
		is_brand_present = True
		for i in range(items_b.count()):
			brand_id.append(items_b[i].id)

	cat_check = check()
	items_c = ProductInformation.objects.filter(category__icontains=cat_check)
	if items_c.count() > 0 :
		is_category_present = True
		for i in range(items_c.count()):
			category_id.append(items_c[i].id)
	items_s = ProductInformation.objects.filter(subSategory__icontains=sub)
	if items_s.count() > 0 :
		is_subCategory_present = True
		for i in range(items__s.count()):
			category_id.append(items_s[i].id)
	print(brand_id)
	print(category_id)
	print(subCategory_id)

def check(item):
	map_cat = {}
	z = ['sandals','slippers','heels','flats','sports shoes','sneakers','loafers','formal shoes','boots']
	for i in z:
		map_cat[i] = 'shoes'
	try:
		return map_cat[item]
	except:
		return 'NULL'