from django.db import models

# Create your models here.
class Device(models.Model):
	#product category attributes
	category = models.CharField("Product Category", blank=True, null=True)
	subCategory = models.CharField("Product Category", blank=True, null=True)
	type = models.CharField("Product Type", blank=True, null=True)
	date_sale = models.DateTimeField("Date of Sale", default=datetime.now, blank=True, null=True)
	gender = models.CharField("Gender", blank=True, null=True)
	
	#product attributes
	price = models.BigIntegerField("Product Price", blank=True, null=True)
	brand = models.CharField("Product Brand", db_index=True, blank=True, null=True)
	listPrice = models.BigIntegerField("Product List Price", blank=True, null=True)
	discount = models.BigIntegerField("Discount", blank=True, null=True)
	name = models.CharField("Product Name", db_index=True, blank=True, null=True)
	url = models.CharField("Product URL", blank=True, null=True)
	description = models.CharField("description", blank=True, null=True)
	availability = models.CharField("Availability", blank=True, null=True)
	color = models.CharField("Colour", blank=True, null=True)
	
	#Rating Attributes
	productRating = models.CharField("Product Rating", blank=True, null=True)
	numberRating = models.BigIntegerField("Rating of the Product", blank=True, null=True)

	#Link attributes
	imageLink = models.CharField("Link of Image", blank=True, null=True)
	androidLink = models.CharField("Android Link", blank=True, null=True)
	referredFrom = models.CharField("Link From Website", blank=True, null=True)