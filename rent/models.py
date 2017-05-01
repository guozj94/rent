# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import random, string

import os
import json

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

def useruploadpath(instance, filename):
	path = "rent/static/rent/user_image"
	format = str(instance.user_id) + '.' + (instance.content_type).split('/')[-1]
	return os.path.join(path, format)

def itemuploadpath(instance, filename):
	path = "rent/static/rent/item_image"
	format = randomword(15) + '.' + (instance.content_type).split('/')[-1]
	return os.path.join(path, format)

# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	photo = models.FileField(upload_to=useruploadpath, blank=True, null=True)
	content_type = models.CharField(max_length=50, blank=True, null=True)
	rate = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)

	def __unicode__(self):
		return 'name=' + str(self.name)

class OfferingItem(models.Model):
	name = models.CharField(max_length=100)
	lender = models.ForeignKey(User)
	picture = models.FileField(upload_to=itemuploadpath, blank=True, null=True)
	content_type = models.CharField(max_length=50, blank=True, null=True)
	description = models.TextField(max_length=300, blank=True, null=True)
	reward = models.CharField(max_length=100, blank=True)
	post_date = models.DateField(auto_now_add=True, blank=True, null=True)
	active = models.BooleanField(default=True, blank=False)
	available_from = models.DateField(blank=True, null=True)
	available_to = models.DateField(blank=True, null=True)

	def __unicode__(self):
		return 'id=' + str(self.id)

class RequestingItem(models.Model):
	name = models.CharField(max_length=100)
	borrower = models.ForeignKey(User)
	picture = models.FileField(upload_to=itemuploadpath, blank=True, null=True)
	content_type = models.CharField(max_length=50, blank=True, null=True)
	description = models.TextField(max_length=300, blank=True, null=True)
	reward = models.CharField(max_length=100, blank=True, null=True)
	post_date = models.DateField(auto_now_add=True, blank=True, null=True)
	active = models.BooleanField(default=True, blank=False)
	need_from = models.DateField(blank=True, null=True)
	need_to = models.DateField(blank=True, null=True)

	def __unicode__(self):
		return 'id=' + str(self.id)

class OfferResponse(models.Model):
	item = models.ForeignKey(OfferingItem)
	borrower = models.ForeignKey(User)
	start_time = models.DateField(blank=True, null=True)
	end_time = models.DateField(blank=True, null=True)
	post_date = models.DateField(auto_now_add=True, blank=True, null=True)
	borrower_note = models.TextField(max_length=300, blank=True)
	reward = models.CharField(max_length=100, blank=True)

	def __unicode__(self):
		return 'id=' + str(self.id)


class RequestResponse(models.Model):
	item = models.ForeignKey(RequestingItem) # item to which are being responded
	responding_item = models.ForeignKey(OfferingItem) # item being offered as a response, if none, user create new one
	lender = models.ForeignKey(User)
	start_time = models.DateField(blank=True, null=True)
	end_time = models.DateField(blank=True, null=True)
	post_date = models.DateField(auto_now_add=True, blank=True, null=True)
	lender_note = models.TextField(max_length=300, blank=True)
	reward = models.CharField(max_length=100, blank=True)

	def __unicode__(self):
		return 'id=' + str(self.id)

class Transaction(models.Model):
	lender = models.ForeignKey(User, related_name='transaction_lend')
	borrower = models.ForeignKey(User, related_name='transaction_borrow')
	is_offer = models.BooleanField(blank=False)
	offer_item = models.ForeignKey(OfferingItem, blank=True, null=True)
	request_item = models.ForeignKey(RequestingItem, blank=True, null=True)
	reward = models.CharField(max_length=100, blank=True, null=True)
	date_of_transaction = models.DateTimeField(auto_now_add=True)
	start_time = models.DateField(blank=True, null=True)
	end_time = models.DateField(blank=True, null=True)
	review_to_lender = models.TextField(max_length=300, blank=True, null=True)
	review_to_borrower = models.TextField(max_length=300, blank=True, null=True)
	rate_to_lender = models.IntegerField(blank=True, default=5)
	rate_to_borrower = models.IntegerField(blank=True, default=5)

	def __unicode__(self):
		return 'id=' + str(self.id)


		