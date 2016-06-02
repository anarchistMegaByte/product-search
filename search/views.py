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


def standard_tags(str_from_tag):

	brand = 'NULL'
	category = 'NULL'
	sub = 'NULL'
	inter = str_from_tag.split(",")
	
	imm = []
	
	for i in inter:
		temp = i.split(":")
		for j in temp:
			j = j.replace(' ','')
			j = j.replace('&amp','')
			j = j.replace('-','')
			j = j.replace('\'s','')
			imm.append(j.lower())
	
	print(imm)

	for i in range(len(imm)):
		if imm[i] == 'brand':
			brand = imm[i+1]
		if imm[i] == 'category':
			category = imm[i+1]
		if imm[i] == 'subcategory':
			sub = imm[i+1]
	
	return (brand,category,sub)


@csrf_exempt
def get_text(request):
	#print(request)
	#print(request.META)
	print((request.body.decode('utf-8')))
	text_from_tags = request.body.decode('utf-8')
	text_from_tags = text_from_tags.replace("'",'"')
	text_in_json = json.loads(text_from_tags)
	string_from_tag = text_in_json['string']#.replace('\n', ' ')
	
	brand,category,sub= standard_tags(string_from_tag)
	
	'''
	#brand names fetched from database
	Brands = []
	a = ProductInformation.objects.all().values_list('brand').distinct()
	for i in a:
		Brands.append(list(i)[0])
	for i in range(len(Brands)):
		Brands[i] = Brands[i].replace(' ','')
		Brands[i] = Brands[i].replace('&amp','')
		Brands[i] = Brands[i].replace('-','')
		Brands[i] = Brands[i].replace('\'s','')
		Brands[i] = Brands[i].lower()

	#Categories fetched from the database
	Categories = []
	c = ProductInformation.objects.all().values_list('category').distinct()
	for i in c:
		Categories.append(list(i)[0])
	for i in range(len(Categories)):
		Categories[i] = Categories[i].lower()

	#subCategories fetched from database
	SubCategories = []
	b = ProductInformation.objects.all().values_list('subCategory').distinct()
	for i in b:
		SubCategories.append(list(i)[0])
	for i in range(len(SubCategories)):
		SubCategories[i] = SubCategories[i].lower()	
	
	#brand names in string from tag matching with the databse brand names
	selected_brands = []
	for j in Brands:
		for i in list_of_text_from_tag:
			if i == j:
				selected_brands.append(i)

	#categories names in string from tag matching with the database Categories names
	selected_categories = []
	for j in Categories:
		for i in list_of_text_from_tag:
			if j==i:
				selected_categories.append(i)

	#subCatefories in string from tag matching with the database subCategories
	selected_subCategories = []
	for j in SubCategories:
		for i in list_of_text_from_tag:
			if i == j:
				selected_subCategories.append(i)
	'''
	'''
	#assigning final values to be passed to algorithm
	if len(selected_brands) != 0:
	    if brand =='NULL':
			brand = selected_brands[0]
	else:
		brand = 'NULL'
		print("selected brands list is 0")

	if len(selected_categories) != 0 and category=='NULL':
		category = selected_categories[0]
	else:
		category = 'NULL'
		print("Selected Categories list is 0")

	if len(selected_subCategories) != 0 and sub=='NULL':
		sub = selected_subCategories[0]
	else:
		sub = 'NULL'
		print("selected subCategories list is Zero")
	'''
	print("Brand=" + brand)
	print("Category=" + category)
	print("subcategory=" + sub)

	#algorithm to get the list of ids from database which match the text from tags
	list_id = algorithm(brand,category,sub)


	#referred from logic
	print(list_id)
	print("------------------" + str(list_id))
    #getting list of products full fillng the requirements as per brand and subcategories
	#list_id = list_id[:10]

	#print("------------------" + str(list_id))
	#returning the dictionary that is to be read at phone
	if len(list_id) != 0:
		return_dict = {}
		count = 1
		for i in list_id:
			products = ProductInformation.objects.filter(pk=i)[:1]
			return_dict[count] = {
							 'Error Code'       : "200"                        ,
							 'id'               : products[0].id               ,
		                     'name'             : products[0].name             ,
		                     'referredFrom'     : products[0].referredFrom     ,
		                     'price'            : products[0].price            ,
		                     'listPrice'        : products[0].listPrice        ,
		                     'imageLink'        : products[0].imageLink        ,
		                     'url'              : products[0].url               }
			count = count + 1 
		#if request.method == 'POST':
			#print(request.body)
		#contents1 = {"name":"Yolo so"	}
	else:
		print("list_id is 0. Therefore error code 404 send")
		return_dict[count+1] = {'Error Code' : "404",
		                        'Message' : "Product Not Found"}
	return JsonResponse(return_dict, safe=False)


@csrf_exempt
def get_results(request):
	products = ProductInformation.objects.filter(pk__gt=10)[:10]
	
	return_dict = {}
	for i in range(len(products.values())):
		return_dict[i+1] = { 'id'               : products[i].auto_id          ,
		                     'name'             : products[i].name             ,
		                     'referredFrom'     : products[i].referredFrom     ,
		                     'price'            : products[i].price            ,
		                     'listPrice'        : products[i].listPrice        ,
		                     'imageLink'        : products[i].imageLink        } 
	#products_list = json.dumps(list(products), cls=DjangoJSONEncoder)
	#products_json = json.loads(products_list)
	return JsonResponse(return_dict, safe=False)

def algorithm(brand, cat, sub):
	'''
	# to check which filter is present False: if not present else True
	is_brand_present = False
	is_category_present = False
	is_subCategory_present = False

	#to store the respective filtered id's
	brand_id = []
	category_id = []
	subCategory_id = []
	'''
	send = []
	three = {}
	two = {}
	
	#all 3 intersection(category,subcategory,brand)
	if sub != 'NULL' and brand != 'NULL' and cat != 'NULL':
		items_s = ProductInformation.objects.filter(category__icontains=cat,subCategory__icontains=sub,brand__icontains = brand)
		if items_s.count() > 0 :
			#is_subCategory_present = True
			for i in range(items_s.count()):
				#subCategory_id.append(items_s[i].auto_id)
				three[items_s[i].id] = items_s[i].listPrice
				#creating one sinle list including both 
				#send.append(items_s[i].auto_id)
		else:
			print("No three intersection found found")
	else:
		print("somthing out of three is null")

	#2 intersection(category,brand)
	if cat != 'NULL' and brand !='NULL':
		items_c = ProductInformation.objects.filter(category__icontains=cat,brand__icontains = brand)
		if items_c.count() > 0 :
			#is_category_present = True
			#print(str(items_c.count()))
			for i in range(items_c.count()):
				#category_id.append(items_c[i].auto_id)
				two[items_c[i].id] = items_c[i].listPrice
				#send.append(items_c[i].auto_id)
		else:
			print("No matching Category found")
	else:
		print("Categorey is NULL")

	sorted_three = []
	gen1 = ((k, three[k]) for k in sorted(three, key=three.get, reverse=False))

	for k,v in gen1:
		sorted_three.append(k)

	print("sortedThree---" + str(sorted_three))

	sorted_two = []
	gen3 = ((k, two[k]) for k in sorted(two, key=two.get, reverse=False))

	for k,v in gen3:
		sorted_two.append(k)

	print("sortedTwo---" + str(sorted_two))

	
	'''
	if brand != 'NULL':
		items_b = ProductInformation.objects.filter(brand__icontains=brand)
		if items_b.count() > 0 :
			is_brand_present = True
			for i in range(items_b.count()):
				brand_id.append(items_b[i].auto_id)
		else:
			print("No matching Brand found")
	else:
		print("Brand is NULL")
	'''

	#print("B" + str(len(brand_id)))
	
	#print("C" + str(len(category_id)))

	#print("S" + str(len(subCategory_id)))

	#print(brand_id)
	#print(category_id)
	#print(subCategory_id)


	'''
	type1 = []
	#logic to send to mobile
	if is_brand_present:
		if is_category_present :
			type1 = list(set(brand_id).intersection(category_id))
		else:
			print("is_category_present is false")	
	else:
		print("is_brand_present is false")
	
	#print(type1)
	
	type2 = []
	if is_brand_present:
		if is_subCategory_present :
			type2 = list(set(brand_id).intersection(subCategory_id))
		else:
			print("is_subCategory_present is false")
	else:
		print("is_brand_present is false")
	
	#print(type2)
	return type1 + type2
	'''

	return sorted_three[:10] + sorted_two[:10]
	
def check(item):
	map_cat = {}
	z = ['sandals','slippers','heels','flats','sports shoes','sneakers','loafers','formal shoes','boots']
	for i in z:
		map_cat[i] = 'shoes'
	try:
		return map_cat[item]
	except:
		return 'NULL'