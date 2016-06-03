import json
from urllib.request import urlopen,Request
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from .models  import ProductInformation

from datetime import datetime
import hmac
import urllib.request
import hashlib
import base64,os
import xmltodict


# Create your views here.

def amazon(name):
	#sign = str(getSignatureKey(key,dateStamp,regionName,serviceName))
	lol = (str(datetime.utcnow())[:-7]+"Z").replace(' ','T')
	inputtext = name
	inputtext = inputtext.replace(' ','%20')
	print(inputtext)

	lol = lol.replace(':','%3A')
	prepend = '''GET
	webservices.amazon.in
	/onca/xml
	'''
	string1 = ["AWSAccessKeyId=AKIAITTECEISJCAEEI6Q","AssociateTag=xynsblo-21","Operation=ItemSearch","ResponseGroup=Large","SearchIndex=All","Version=2011-08-01","Keywords="+inputtext,"Timestamp="+lol,"Service=AWSECommerceService"]
	add = '&'.join(sorted(string1))
	x = prepend+add
	#print x
	secretAccessKey = b"nkKa3NvjwrqsTRneTwMMRGDkfNkK8hcj4pC3nVLB"
	sign = base64.b64encode(hmac.new(secretAccessKey,msg=x.encode('utf-8'), digestmod=hashlib.sha256).digest())
	sign = sign.decode('utf-8')
	sign = sign.replace('+',"%2B")
	sign = sign.replace('=','%3D')
	sign = sign.replace(':',"%3A")
	sign = sign.rstrip('\n')
	print(sign)
	z = "http://webservices.amazon.in/onca/xml?"+add+"&Signature="+sign
	print(z)

	req = Request(z)
	req.add_header('Operation','ItemLookup')
	resp = urlopen(req).read().decode('utf-8')
	print (resp)
	#li = []
	#for x in resp:
	#	li.append(str(x))
	f = open("temporary.xml","w")
	f.write(resp)
	f.close()
	#print li[0]
	# tree = ET.parse('temporary.xml')
	# root = tree.getroot()
	# for x in root.findall('{http://webservices.amazon.com/AWSECommerceService/2011-08-01}Items'):
	# 	for y in x.findall('{http://webservices.amazon.com/AWSECommerceService/2011-08-01}Item'):
	# 		for z in y.find('{http://webservices.amazon.com/AWSECommerceService/2011-08-01}ItemAttributes'):
	# 			print z.tag,
	totallist = []
	try:
		with open('temporary.xml') as fd:
		    doc = xmltodict.parse(fd.read())    
		#print("lol")
		fd.close()    
		print (len(doc['ItemSearchResponse']['Items']['Item']))
		for number in range(len(doc['ItemSearchResponse']['Items']['Item'])):
			print("WTF")
			temp = []
			try:
				try:  
					temp.append(doc['ItemSearchResponse']['Items']['Item'][number]['ItemAttributes']['Binding'])#Category
				except Exception as e:	
					temp.append("null")
					print(e)
					print("\n")
				try:
					temp.append(doc['ItemSearchResponse']['Items']['Item'][number]['ItemAttributes']['ProductGroup'])#subCategory/Type
				except Exception as e:
					temp.append("null")	
					print(e)
					print("\n")
				try:
					temp.append(doc['ItemSearchResponse']['Items']['Item'][number]['ItemAttributes']['ProductTypeName'])#subCategory/Type
				except Exception as e:
					print(e)
					temp.append("null")	
					print("\n")
				try:
					gen = doc['ItemSearchResponse']['Items']['Item'][number]['ItemAttributes']['Department']
					if gen =='Men' or gen == 'mens' or gen=='Mens' or gen=='men':
						gen = 'M'
					elif gen == 'Female' or gen=='female' or gen == 'women' or gen=='womens' or gen=='Women' or gen =='Womens':
						gen = 'F'
					else:
						gen = 'B'	
					temp.append(gen)
							
				except Exception as e:	
					print(e)
					temp.append("B")
					print("\n")
				try:
					p = doc['ItemSearchResponse']['Items']['Item'][number]['Offers']['Offer']['OfferListing']['Price']['Amount'][:-2]#price
					temp.append(p)
				except Exception as e:
					print(e)
					temp.append("null")
					print("\n")
				try:	
					temp.append(doc['ItemSearchResponse']['Items']['Item'][number]['ItemAttributes']['Brand'])#Brand
				except Exception as e:
					print(e)
					temp.append("null")
					print("\n")
				try:
					lp = doc['ItemSearchResponse']['Items']['Item'][number]['OfferSummary']['LowestNewPrice']['Amount'][:-2]#listPrice
					temp.append(lp)
				except Exception as e:
					print(e)
					temp.append("null")
					print("\n")				
				try:
					temp.append(str(((((int(p)-int(lp))*100)/int(p))))+"%")#Discount
				except Exception as e:
					print(e)
					temp.append("null")	
					print("\n")
				try:
					temp.append(doc['ItemSearchResponse']['Items']['Item'][number]['ItemAttributes']['Title'])#Name
				except Exception as e:	
					print(e)
					temp.append("null")
					print("\n")
				try:  
					temp.append(doc['ItemSearchResponse']['Items']['Item'][number]['DetailPageURL'])#URL
				except Exception as e:	
					print(e)
					temp.append("null")
					print("\n")
				try:
					temp.append(doc['ItemSearchResponse']['Items']['Item'][number]['ItemAttributes']['Feature'][-1])#Description
				except Exception as e:
					print(e)
					temp.append("null")
					print("\n")
				try:
					av = doc['ItemSearchResponse']['Items']['Item'][number]['Offers']['Offer']['OfferListing']['AvailabilityAttributes']['AvailabilityType']#availability
					if av == 'now':
						temp.append('True')
					else:
						temp.append('False')	
				except Exception as e:
					print(e)
					temp.append("null")	
					print("\n")			
				try:	
					temp.append(doc['ItemSearchResponse']['Items']['Item'][number]['ItemAttributes']['Color'])#Color
				except Exception as e:	
					print(e)
					temp.append("null")
					print("\n")
				try:	
					temp.append(doc['ItemSearchResponse']['Items']['Item'][number]['CustomerReviews']['IFrameURL'])		
				except Exception as e:	
					print(e)
					temp.append("null")
					print("\n")
				temp.append("null")
				try:
					temp.append(doc['ItemSearchResponse']['Items']['Item'][number]['MediumImage']['URL'])#imageLink
				except:
					try:
						temp.append(doc['ItemSearchResponse']['Items']['Item'][number]['TinyImage']['URL'])
					except Exception as e:
						print(e)
						temp.append("null")
						print("\n")
				temp.append("null")						
				temp.append("Amazon")
			except Exception as e:
				print(e)
				continue
			#print(temp)	
			totallist.append(temp)
			#print(totallist)		
	except Exception as e:
		print(e)
	#print (len(totallist))	
	for x in totallist:
		print(x)
		print("\n")	
	return totallist		


def flipkart(name):
	headers = (('Fk-Affiliate-Id','ankitbhag2'),('Fk-Affiliate-Token','41deb6213a0a4186bc249966312ed990'))
	#x = input()
	x = name
	print(x)
	x = x.replace(' ','+')
	count = "5"
	url = 'https://affiliate-api.flipkart.net/affiliate/search/json?query='+x+'&resultCount='+count
	req = Request(url)
	req.add_header('Fk-Affiliate-Id','ankitbhag2')
	req.add_header('Fk-Affiliate-Token','41deb6213a0a4186bc249966312ed990')
	resp = urlopen(req).read().decode('utf-8')
	json_list = []
	#print type(resp)
	#for x in resp:
	#	json_list.append(x)
	#print(json_list)	
	#print json_list[0]
	totallist = []
	data = json.loads(resp)
	for _ in range(len(data['productInfoList'])):
		try:	
			temp = []
			lis = data['productInfoList'][_]['productBaseInfo']['productIdentifier']['categoryPaths']['categoryPath'][0][0]['title'].split('>')
			li = [x.lower() for x in lis]
				
			#print lis		
			temp.append(lis[0])#Category
			temp.append("null")
			#Subcategory Scene
			temp.append(lis[-1])#Type
			if 'men' in li or 'boys' in li or 'man' in li:
				temp.append("M")
			elif 'women' in li or 'girls' in li or 'woman' in li:
				temp.append("F")
			else:
				temp.append("B")
			temp.append(data['productInfoList'][_]['productBaseInfo']['productAttributes']['maximumRetailPrice']['amount'])#MRP	
			temp.append(data['productInfoList'][_]['productBaseInfo']['productAttributes']['productBrand'])#Brand
			temp.append(data['productInfoList'][_]['productBaseInfo']['productAttributes']['sellingPrice']['amount'])#Selling Price
			temp.append(data['productInfoList'][_]['productBaseInfo']['productAttributes']['discountPercentage'])#discount
			temp.append(data['productInfoList'][_]['productBaseInfo']['productAttributes']['title'])#Name
			temp.append(data['productInfoList'][_]['productBaseInfo']['productAttributes']['productUrl'])#Url
			temp.append(data['productInfoList'][_]['productBaseInfo']['productAttributes']['productDescription'])#Description
			temp.append(data['productInfoList'][_]['productBaseInfo']['productAttributes']['inStock'])#availability
			temp.append(data['productInfoList'][_]['productBaseInfo']['productAttributes']['color'])#color
			temp.extend(["null","null"])
			temp.append(data['productInfoList'][_]['productBaseInfo']['productAttributes']['imageUrls']['400x400'])#imageLink
			temp.append("null")
			temp.append("Flipkart")
			totallist.append(temp)
			print("\n")
		except Exception as e:
			print(e)
	#for lol in totallist:
		#print (lol)
		#print ("\n")
	#print("$$$$$$$$$$$$$$$4----" + str(totallist.sort(key=lambda x: x[6])))

	return totallist


def search_flipkart(request):
	'''
	equest = urllib.request.Request("https://affiliate-api.flipkart.net/affiliate/search/json?query=adidas+golf+shoes&resultCount=5")
	equest.add_header('Fk-Affiliate-Id', 'ankitbhag2')
	equest.add_header('Fk-Affiliate-Token','41deb6213a0a4186bc249966312ed990')
	contents = urllib.request.urlopen(equest).read().decode("utf-8")
	#return HttpResponse(html)
	return JsonResponse(contents,safe=False)
	'''
	headers = (('Fk-Affiliate-Id','ankitbhag2'),('Fk-Affiliate-Token','41deb6213a0a4186bc249966312ed990'))
	#x = input()
	x = "nike casual shoes"
	x = x.replace(' ','+')
	count = "5"
	url = 'https://affiliate-api.flipkart.net/affiliate/search/json?query='+x+'&resultCount='+count
	req = Request(url)
	req.add_header('Fk-Affiliate-Id','ankitbhag2')
	req.add_header('Fk-Affiliate-Token','41deb6213a0a4186bc249966312ed990')
	resp = urlopen(req).read().decode('utf-8')
	json_list = []
	#print type(resp)
	#for x in resp:
	#	json_list.append(x)
	#print(json_list)	
	#print json_list[0]
	totallist = []
	data = json.loads(resp)
	for _ in range(len(data['productInfoList'])):
		try:	
			temp = []
			lis = data['productInfoList'][_]['productBaseInfo']['productIdentifier']['categoryPaths']['categoryPath'][0][0]['title'].split('>')
			li = [x.lower() for x in lis]
				
			#print lis		
			temp.append(lis[0])#Category
			temp.append("null")
			#Subcategory Scene
			temp.append(lis[-1])#Type
			if 'men' in li or 'boys' in li or 'man' in li:
				temp.append("M")
			elif 'women' in li or 'girls' in li or 'woman' in li:
				temp.append("F")
			else:
				temp.append("B")
			temp.append(data['productInfoList'][_]['productBaseInfo']['productAttributes']['maximumRetailPrice']['amount'])#MRP	
			temp.append(data['productInfoList'][_]['productBaseInfo']['productAttributes']['productBrand'])#Brand
			temp.append(data['productInfoList'][_]['productBaseInfo']['productAttributes']['sellingPrice']['amount'])#Selling Price
			temp.append(data['productInfoList'][_]['productBaseInfo']['productAttributes']['discountPercentage'])#discount
			temp.append(data['productInfoList'][_]['productBaseInfo']['productAttributes']['title'])#Name
			temp.append(data['productInfoList'][_]['productBaseInfo']['productAttributes']['productUrl'])#Url
			temp.append(data['productInfoList'][_]['productBaseInfo']['productAttributes']['productDescription'])#Description
			temp.append(data['productInfoList'][_]['productBaseInfo']['productAttributes']['inStock'])#availability
			temp.append(data['productInfoList'][_]['productBaseInfo']['productAttributes']['color'])#color
			temp.extend(["null","null"])
			temp.append(data['productInfoList'][_]['productBaseInfo']['productAttributes']['imageUrls']['400x400'])#imageLink
			temp.append("null")
			temp.append("Flipkart")
			totallist.append(temp)
			print("\n")
		except Exception as e:
			print(e)
	for lol in totallist:
		print (lol)
		print ("\n")

	contents1 = {"name":"Yolo so"	}
	return JsonResponse(contents1, safe=False)


def standard_tags(str_from_tag):

	brand = 'NULL'
	category = 'NULL'
	sub = 'NULL'
	price = 0
	name = 'NULL'
	types = 'NULL'
	inter = str_from_tag.split(",")
	name1 = 'NULL'
	imm = []
	
	for i in inter:
		temp = i.split(":")
		for j in range(len(temp)):
			temp1 = temp[j].replace(' ','')
			if temp1 == 'Name':
				name1 = temp[j+1]
				#print("CHuttttttttttttt----"+name1+"----"+temp[j])
			temp[j]= temp[j].replace(' ','')
			temp[j] = temp[j].replace('&amp','')
			temp[j] = temp[j].replace('-','')
			temp[j] = temp[j].replace('\'s','')
			imm.append(temp[j].lower())
	
	print(imm)

	for i in range(len(imm)):
		if imm[i] == 'brand':
			brand = imm[i+1]
		if imm[i] == 'category':
			category = imm[i+1]
		if imm[i] == 'subcategory':
			sub = imm[i+1]
		if imm[i] == 'price':
			price=imm[i+1]
		if imm[i] == 'name':
			name = imm[i+1]
		if imm[i] == 'type' :
			types = imm[i+1]
	
	return (brand,category,sub,price,name,types,name1)


@csrf_exempt
def get_text(request):
	#print(request)
	#print(request.META)
	print((request.body.decode('utf-8')))
	text_from_tags = request.body.decode('utf-8')
	text_from_tags = text_from_tags.replace("'",'"')
	text_in_json = json.loads(text_from_tags)
	string_from_tag = text_in_json['string']#.replace('\n', ' ')
	
	brand,category,sub,price,name,types,name1 = standard_tags(string_from_tag)
	
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
	print("price="+str(price))
	print("name="+name)
	print("Type="+types)

	#algorithm to get the list of ids from database which match the text from tags
	flipkart_list,list_id = algorithm(brand,category,sub,price,name,types,name1)

	print("------------------"  + str(flipkart_list))

	#print("------------------"  + str(amazon_list))
	#referred from logic
	print("------------------" + str(list_id))
    #getting list of products full fillng the requirements as per brand and subcategories
	#list_id = list_id[:10]

	#print("------------------" + str(list_id))
	#returning the dictionary that is to be read at phone
	count = 1
	return_dict = {}
	if len(list_id) != 0:
		for i in list_id:
			products = ProductInformation.objects.filter(pk=i)[:1]
			#print(products[0].listPrice)
			return_dict[count] = {
							 'Error Code'       : "200"                        ,
							 'id'               : products[0].auto_id          ,
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
		return_dict[0] = {'Error Code' : "404",
		                        'Message' : "Product Not Found"}

	if len(flipkart_list)>0:
		for i in flipkart_list:
			return_dict[count] = {
							 'Error Code'       : "200"                        ,
							 'id'               : count          			   ,
		                     'name'             : i[8]             ,
		                     'referredFrom'     : i[17]     ,
		                     'price'            : i[4]            ,
		                     'listPrice'        : i[6]        ,
		                     'imageLink'        : i[15]        ,
		                     'url'              : i[9]               }
			count = count + 1
	'''
	if len(amazon_list)>0:
		for i in amazon_list:
			return_dict[count] = {
							 'Error Code'       : "200"                        ,
							 'id'               : count          			   ,
		                     'name'             : i[8]             ,
		                     'referredFrom'     : i[17]     ,
		                     'price'            : i[4]            ,
		                     'listPrice'        : i[6]        ,
		                     'imageLink'        : i[15]        ,
		                     'url'              : i[9]               }
			count = count + 1
	'''
	return JsonResponse(return_dict, safe=False)


@csrf_exempt
def get_results(request):
	products = ProductInformation.objects.filter(pk__gt=10)[:10]
	
	return_dict = {}
	for i in range(len(products.values())):
		return_dict[i+1] = { 'id'               : products[i].id        ,
		                     'name'             : products[i].name             ,
		                     'referredFrom'     : products[i].referredFrom     ,
		                     'price'            : products[i].price            ,
		                     'listPrice'        : products[i].listPrice        ,
		                     'imageLink'        : products[i].imageLink        } 
	#products_list = json.dumps(list(products), cls=DjangoJSONEncoder)
	#products_json = json.loads(products_list)
	return JsonResponse(return_dict, safe=False)

def algorithm(brand, cat, sub,price,name,types,name1):
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
	three_j = {}
	three_p = {}
	#two_j = {}
	#two_p = {}
	
	#all 3 intersection(category,subcategory,brand)
	if sub != 'NULL' and brand != 'NULL' and cat != 'NULL':
		#brand,cat,sub,price,jabong
		items_s = ProductInformation.objects.filter(category__icontains=cat,subCategory__icontains=sub,brand__icontains = brand,referredFrom__icontains='Jabong',price__icontains=price)
		if len(items_s) > 0 :
			for i in range(len(items_s)):
				three_j[items_s[i].auto_id] = items_s[i].listPrice
		else:
			#brand,cat,sub,productname,jabong
			items_s = ProductInformation.objects.filter(category__icontains=cat,subCategory__icontains=sub,brand__icontains = brand,referredFrom__icontains='Jabong',name__icontains=name)
			if len(items_s) > 0:
				for i in range(len(items_s)):
					three_j[items_s[i].auto_id] = items_s[i].listPrice
			else:
				#brand,cat,sub,jabong
				items_s = ProductInformation.objects.filter(category__icontains=cat,subCategory__icontains=sub,brand__icontains = brand,referredFrom__icontains='Jabong')
				if len(items_s) > 0:
					for i in range(len(items_s)):
						three_j[items_s[i].auto_id] = items_s[i].listPrice
				else:
					#brand,cat,jabong
					items_s = ProductInformation.objects.filter(category__icontains=cat,brand__icontains = brand,referredFrom__icontains='Jabong')
					if len(items_s) > 0:
						for i in range(len(items_s)):
							three_j[items_s[i].auto_id] = items_s[i].listPrice
					else:
						print("Nothing found ! no intresections possible")


	#all 3 intersection(category,subcategory,brand)
	if sub != 'NULL' and brand != 'NULL' and cat != 'NULL':
		#brand,cat,sub,price,paytm
		items_s = ProductInformation.objects.filter(category__icontains=cat,subCategory__icontains=sub,brand__icontains = brand,referredFrom__icontains='PayTM',price__icontains=price)
		if len(items_s) > 0 :
			for i in range(len(items_s)):
				three_p[items_s[i].auto_id] = items_s[i].listPrice
		else:
			#brand,cat,sub,productname,jabong
			items_s = ProductInformation.objects.filter(category__icontains=cat,subCategory__icontains=sub,brand__icontains = brand,referredFrom__icontains='PayTM',name__icontains=name)
			if len(items_s) > 0:
				for i in range(len(items_s)):
					three_p[items_s[i].auto_id] = items_s[i].listPrice
			else:
				#brand,cat,sub,jabong
				items_s = ProductInformation.objects.filter(category__icontains=cat,subCategory__icontains=sub,brand__icontains = brand,referredFrom__icontains='PayTM')
				if len(items_s) > 0:
					for i in range(len(items_s)):
						three_p[items_s[i].auto_id] = items_s[i].listPrice
				else:
					#brand,cat,jabong
					items_s = ProductInformation.objects.filter(category__icontains=cat,brand__icontains = brand,referredFrom__icontains='PayTM')
					if len(items_s) > 0:
						for i in range(len(items_s)):
							three_p[items_s[i].auto_id] = items_s[i].listPrice
					else:
						print("Nothing found ! no intresections possible")		


	#flipkart results
	
	if name1!='NULL':
		flipkart_list = flipkart(name1)
		#amazon_list = amazon(name1)
		#print("###############" + str(amazon_list))
	else:
		if brand!='NULL':
			if types!='NULL':
				flipkart_list = flipkart(brand+" "+types)
				#amazon_list = amazon(brand+" "+types)
			else:
				if cat!='NULL':
					if sub!='NULL':
						flipkart_list = flipkart(brand+" "+cat+" "+sub)
						#amazon_list = amazon(brand+" "+cat+" "+sub)

					else:
						flipkart_list = flipkart(brand+" "+cat)
						#amazon_list = amazon(brand+" "+cat)
				else:
					if sub!='NULL':
						flipkart_list = flipkart(brand+" "+sub)
						#amazon_list = amazon(brand+" "+sub)
					else:
						flipkart_list = flipkart(brand)
						#amazon_list = amazon(brand)
		else:
			if types!='NULL':
				flipkart_list = flipkart(types)
				#amazon_list = amazon(types)
			else:
				if category!='NULL':
					if sub!='NULL':
						flipkart_list = flipkart(cat+" "+sub)
						#amazon_list = amazon(cat+" "+sub)
					else:
						flipkart_list = flipkart(cat)
						#amazon_list = amazon(cat)
				else:
					if sub!='NULL':
						flipkart_list = flipkart(sub)
						#amazon_list = amazon(sub)
					else:
						print("NO products possible")
						flipkart_list = []
						#amazon_list = []

	'''
		items_s = ProductInformation.objects.filter(category__icontains=cat,subCategory__icontains=sub,brand__icontains = brand,referredFrom__icontains='PayTM')
		if len(items_s) > 0 :
			#is_subCategory_present = True
			for i in range(len(items_s)):
				three_p[items_s[i].auto_id] = items_s[i].listPrice
				#subCategory_id.append(items_s[i].auto_id)
				#print(str(items_s[i].auto_id) + "    " + str(items_s[i].listPrice))
				
				#creating one sinle list including both 
				#send.append(items_s[i].auto_id)
		else:
			print("No three intersection found for paytm")
	else:
		print("somthing out of three is null")

	if len(three_j)==0:
	#2 intersection(category,brand),r,refe
		if cat != 'NULL' and brand !='NULL':
			items_c = ProductInformation.objects.filter(category__icontains=cat,brand__icontains = brand,referredFrom__icontains='Jabong')
			if len(items_c) > 0 :
			#is_category_present = True
			#print(str(items_c.count()))
				for i in range(len(items_c)):
				#category_id.append(items_c[i].auto_id)
					two_j[items_c[i].auto_id] = items_c[i].listPrice
				#send.append(items_c[i].auto_id)
			else:
				print("No matching Category found")
		else:
			print("Categorey is NULL")

	if len(three_p) == 0:
		if cat != 'NULL' and brand !='NULL':
			items_c = ProductInformation.objects.filter(category__icontains=cat,brand__icontains = brand,referredFrom__icontains='PayTM')
			if len(items_c) > 0 :
			#is_category_present = True
			#print(str(items_c.count()))
				for i in range(len(items_c)):
				#category_id.append(items_c[i].auto_id)
					two_p[items_c[i].auto_id] = items_c[i].listPrice
				#send.append(items_c[i].auto_id)
			else:
				print("No matching Category found")
		else:
			print("Categorey is NULL")		
	#print(three)
	#print(two)	

	sorted_three = []
	sorted_three_values = []

	gen1 = ((k, three[k]) for k in sorted(three, key=three.get, reverse=False))

	for k,v in gen1:
		sorted_three.append(k)
		sorted_three_values.append(v)

	print("sortedThree---" + str(sorted_three_values))
	
	sorted_two = []
	sorted_two_values = []
	gen3 = ((k, two[k]) for k in sorted(two, key=two.get, reverse=False))

	for k,v in gen3:
		sorted_two_values.append(v)
		sorted_two.append(k)

	print("sortedTwo---" + str(sorted_two_values))
	'''
	'''
	if len(three_j) !=0 :
		sorted_three__values_j = sorted(three_j.values())
		sorted_three_keys_j = sorted(three_j,key=three_j.get)
		send = send + sorted_three_keys_j
	if len(three_p) != 0:
		sorted_three_values_p = sorted(three_p.values())
		sorted_three_keys_p = sorted(three_p,key=three_p.get)
		send = send + sorted_three_keys_p

	if len(two_j) != 0:
		sorted_two_values_j = sorted(two_j.values())
		sorted_two_keys_j = sorted(two_j,key=two_j.get)
		send = send + sorted_two_keys_j
	if len(two_p) != 0:
		sorted_two_values_p = sorted(two_p.values())
		sorted_two_keys_p = sorted(two_p,key=two_p.get)
		send = send + sorted_two_keys_p
	'''

	sorted_three_j = sorted(three_j,key=three_j.get)
	sorted_three_p = sorted(three_p,key=three_p.get)
		
	if len(sorted_three_j) > 10 :
		send = send + sorted_three_j[:10]
	else:
		send = send + sorted_three_j
	if len(sorted_three_p) > 10:
		send = send + sorted_three_p[:10]
	else:
		send = send + sorted_three_p
	#print(str(three.keys()))
	#print(str(sorted_tree_keys))
	#print(str(sorted_three_values))
	#print(str(sorted_two_keys))
	#print(str(sorted_two_values))

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
	return flipkart_list,send

	
def check(item):
	map_cat = {}
	z = ['sandals','slippers','heels','flats','sports shoes','sneakers','loafers','formal shoes','boots']
	for i in z:
		map_cat[i] = 'shoes'
	try:
		return map_cat[item]
	except:
		return 'NULL'