from django.shortcuts import render
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ParseError
from rest_framework import status
from django.contrib.auth.models import User
from .models import UserProfile

from datetime import datetime


# Create your views here.
def _return_json_value(sample_dict, key):
	if key in sample_dict:
		return sample_dict[key]
	else:
		return None


@csrf_exempt
def register_and_tokenize(request):
	"""
	Register a new user to the UserProfile table
	"""
	if request.method == 'POST':
		received_json_data = json.loads(request.body.decode('utf-8'))
		
		try:
			user = User.objects.create_user(_return_json_value(received_json_data,'userName'), _return_json_value(received_json_data,'userEmail'), _return_json_value(received_json_data,'userPassword'))
		except:
			return JsonResponse({"Response": "Invalid User Attributes"})
		
		#printing attributes
		print (" Mobile Number " + _return_json_value(received_json_data,'userPhone'))
		sample = UserProfile(
							user = user,
							mobile_no = _return_json_value(received_json_data,'userPhone'),
							)
		sample.save()
		token = Token.objects.get_or_create(user=user)
		return JsonResponse({"token": token[0].key, "Status" : "Login Successfull"})
	else:
		return JsonResponse({"Response": "Invalid Method: should be a POST "})