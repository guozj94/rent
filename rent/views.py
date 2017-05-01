# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.db import transaction
from django.contrib import messages
from django.core import serializers
from django.views.decorators.csrf import ensure_csrf_cookie
from rent.models import *
from datetime import datetime
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_aware
import time
import json
import sys
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

# from storages.backends.s3boto import S3BotoStorage
from django.conf import settings
from django.template.loader import render_to_string
# Create your views here.

def home(request):
	return render(request, 'rent/home.html', {})

def search(request):
	context = {}
	keyword = request.GET.get('searchbar', False)
	all_items = OfferingItem.objects.filter(name__contains=keyword)
	print all_items
	context['items'] = all_items
	help_peer = RequestingItem.objects.all()[:3]
	context['help_peer'] = help_peer
	return render(request, 'rent/search.html', context)

def help_peer_detail(request, id):
	if not request.GET or not id:
		return redirect('search')
	context = {}
	request_item = RequestingItem.objects.get(id=id)
	context['request_item'] = request_item
	return render(request, 'rent/helpout.html', context)

def search_ajax(request):
	keyword = request.GET.get('keyword', False)
	all_items = OfferingItem.objects.filter(name__contains=keyword)
	jsonobj = serializers.serialize('json', all_items)
	print jsonobj
	return HttpResponse(jsonobj, content_type='application/json')

def get_datetime(date_str):
	ret = parse_datetime(date_str)
	if not is_aware(ret):
		ret = make_aware(ret)
	return ret


def send_request_ajax(request):
	request_item = RequestingItem()
	if not request.POST:
		context = {'error': ['Oh an error occurs! Please make a request again.']}
		return render(request, 'rent/search.html', context)
	name = request.POST.get('name', False)
	description = request.POST.get('description', False)
	reward = request.POST.get('reward', False)
	need_from = request.POST.get('from', False)
	need_to = request.POST.get('to', False)
	if need_from:
		need_from = need_from[:10]
		need_from = datetime.strptime(need_from, "%m/%d/%Y").date()
		request_item.need_from = need_from
	if need_to:
		need_to = need_to[:10]
		need_to = datetime.strptime(need_to, "%m/%d/%Y").date()
		request_item.need_to = need_to
	request_item.name = name
	request_item.description = description
	request_item.reward = reward
	request_item.borrower = User.objects.get(id=1) #request.user
	request_item.save()
	print name, description, need_from, need_to
	data = []
	jsonobj = json.dumps(data, cls=DjangoJSONEncoder)
	return HttpResponse(jsonobj, content_type='application/json')

def incomingoffer(request):
	context = {}
	my_items = OfferingItem.objects.filter(lender__pk=1) #request.user is_avtive
	incoming_offer = OfferResponse.objects.filter(item__in=my_items)
	context['incoming_offer'] = incoming_offer
	print my_items, incoming_offer
	return render(request, 'rent/myoffers-incoming.html', context)

def confirmedoffer(request):
	context = {}
	my_items = OfferingItem.objects.filter(lender__pk=1) #request.user is_active
	confirmed_offer = Transaction.objects.filter(is_offer=True, offer_item__in=my_items)
	context['confirmed_offer'] = confirmed_offer
	print confirmed_offer
	return render(request, 'rent/myoffers-confirmed.html', context)

def myalloffer(request):
	context = {}
	my_items = OfferingItem.objects.filter(lender__pk=1) #request.user is_active
	context['my_items'] = my_items
	return render(request, 'rent/myoffers-myitems.html', context)

def get_user_photo(request, id):
	user = get_object_or_404(User, id=id)
	print user.profile.photo
	if not user.profile.photo:
		raise Http404
	return HttpResponse(user.profile.photo, content_type=user.profile.content_type)

def get_item_photo(request, id):
	item = get_object_or_404(OfferingItem, id=id)
	if not item.picture:
		raise Http404
	return HttpResponse(item.picture, content_type=item.content_type)
