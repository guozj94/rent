# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
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
from rent.forms import *

# Create your views here.

def landing(request):
	context = {}
	print (request.user)
	form = LoginForm()
	context['form'] = form
	form_reg = RegistrationForm()
	context['form_reg'] = form_reg
	if request.user.is_anonymous():
		context['login'] = 'Log In'
		context['signup'] = 'Sign Up'
	else:
		return render(request, 'rent/home.html',{})
	return render(request, 'rent/index.html', context)


def home(request):
	print(request.user)
	return render(request, 'rent/home.html',{})

def search(request):
	if not request.user.is_authenticated:
		return redirect(reverse('home'))
	context = {}
	keyword = request.GET.get('searchbar', False)
	all_items = OfferingItem.objects.filter(name__contains=keyword)
	#print all_items
	context['items'] = all_items
	help_peer = RequestingItem.objects.all().exclude(borrower=request.user)[:4]
	#print(help_peer)
	context['help_peer'] = help_peer
	return render(request, 'rent/search.html', context)

@login_required
def help_peer_detail(request, id):
	#print request.GET, id
	if not id:
		return redirect('search')
	context = {}
	request_item = RequestingItem.objects.get(id=id)
	print(request_item.name)
	context['request_item'] = request_item
	my_items = OfferingItem.objects.filter(lender=request.user) #request.user is_active
	context['my_items'] = my_items
	return render(request, 'rent/helpout.html', context)

@login_required
@transaction.atomic
def submit_offer(request):
	if request.method != 'POST':
		return redirect('search')
	response = RequestResponse()
	item = RequestingItem.objects.get(id=request.POST.get('requestingItem', False))
	responding_item = OfferingItem.objects.get(id=request.POST.get('selectItem', False))
	lender = responding_item.lender # dummy, you can delete, but beware of the data in database
	reward = responding_item.reward
	response.item = item
	response.responding_item =responding_item
	response.lender = lender
	response.reward = reward
	#print item, responding_item, lender, reward
	response.save()
	data = []
	jsonobj = json.dumps(data, cls=DjangoJSONEncoder)
	return HttpResponse(jsonobj, content_type='application/json')

@login_required
def add_new(request):
	if request.method != 'GET':
		return redirect('search')
	context = {}
	context['request_item_id'] = request.GET.get('requestid', False)
	if not context['request_item_id']:
		return redirect('search')
	return render(request, 'rent/add_new.html', context)

@login_required
def search_ajax(request):
	keyword = request.GET.get('keyword', False)
	all_items = OfferingItem.objects.filter(name__contains=keyword)
	jsonobj = serializers.serialize('json', all_items)
	#print jsonobj
	return HttpResponse(jsonobj, content_type='application/json')

@login_required
def get_datetime(date_str):
	ret = parse_datetime(date_str)
	if not is_aware(ret):
		ret = make_aware(ret)
	return ret

@login_required
@transaction.atomic
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
	request_item.borrower = User.objects.get(id=request.user.id) #request.user
	request_item.save()
	#print name, description, need_from, need_to
	data = []
	jsonobj = json.dumps(data, cls=DjangoJSONEncoder)
	return HttpResponse(jsonobj, content_type='application/json')

@login_required
def incomingoffer(request):
	context = {}
	my_items = OfferingItem.objects.filter(lender=request.user) #request.user is_avtive
	incoming_offer = OfferResponse.objects.filter(item__in=my_items)
	context['incoming_offer'] = incoming_offer
	#print my_items, incoming_offer
	return render(request, 'rent/myoffers-incoming.html', context)

@login_required
def confirmedoffer(request):
	context = {}
	my_items = OfferingItem.objects.filter(lender=request.user) #request.user is_active
	confirmed_offer = Transaction.objects.filter(is_offer=True, offer_item__in=my_items)
	context['confirmed_offer'] = confirmed_offer
	#print confirmed_offer
	return render(request, 'rent/myoffers-confirmed.html', context)

@login_required
def myalloffer(request):
	context = {}
	my_items = OfferingItem.objects.filter(lender=request.user) 
	#request.user is_active
	context['my_items'] = my_items

	return render(request, 'rent/myoffers-myitems.html', context)

@login_required
def get_user_photo(request, id):
	user = get_object_or_404(User, id=id)
	#print user.profile.photo
	if not user.profile.photo:
		raise Http404
	return HttpResponse(user.profile.photo, content_type=user.profile.content_type)

@login_required
def get_item_photo(request, id):
	item = get_object_or_404(OfferingItem, id=id)
	if not item.picture:
		raise Http404
	return HttpResponse(item.picture, content_type=item.content_type)

@login_required
@transaction.atomic
def offer_item(request):
	user = get_object_or_404(Profile, user=request.user)
	context={}
	form = OfferNewItem(request.POST, request.FILES, instance=user)
	if not form.is_valid():
		context['form'] = form
		print("form not valid")
		return render(request, 'rent/add_new.html', context)
	
	
	new_item = OfferingItem(name=form.cleaned_data['name'],
							lender=request.user,
							picture=form.cleaned_data['picture'],
							description=form.cleaned_data['description'],
							reward=form.cleaned_data['reward']) 
	new_item.content_type = form.cleaned_data['picture'].content_type
	new_item.save()

	return redirect(reverse('myalloffer'))

# modal for user account activities: login/register
def login_modal(request):
	context = {}
	print (request.user)
	form = LoginForm()
	context['form'] = form
	form_reg = RegistrationForm()
	context['form_reg'] = form_reg
	return render(request, 'rent/index.html', context)

def login_authenticate(request):
	if request.method != 'POST':
		return redirect(reverse('login'))
	context = {}
	user = User()
	form = LoginForm(request.POST)
	if not form.is_valid():
		context['form'] = form
		return render(request, 'rent/index.html', context)
	#print form.cleaned_data['password']
	user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
	login(request, user)
	return redirect(reverse('home'))

def logout_user(request):
	logout(request)
	landing()

def register_action(request):
	if request.method != 'POST':
		return redirect(reverse('login'))
	form = RegistrationForm(request.POST)
	context['form_reg'] = form
	if not form.is_valid():
		return render(request, 'rent/index.html', context)
	new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password1'],
                                        #email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
	new_user.save()
	new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])
	login(request, new_user)
	return redirect(reverse('home'))

@transaction.atomic
def register(request):
    context = {}

    if request.method == 'GET':
        context['form'] = RegistrationForm()

        return render(request, 'rent/register.html', context)

    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
    	print("registration not valid")
    	return render(request, 'rent/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password1'],
                                        #email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()
    new_profile = Profile(user=new_user)
    new_profile.save()
    
    # Logs in the new user and redirects to his/her todo list
    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])
    login(request, new_user)
    return redirect(reverse('home'))

@login_required
def my_requests(request):
	context = {}
	requested_items = RequestingItem.objects.filter(borrower=request.user)
	context['items'] = []
	request_count = requested_items.count()
	context['count'] = request_count
	for i in range(0,requested_items.count()):
		item_dict = {}
		item_dict['name'] = requested_items[i].name
		item_dict['reward'] = requested_items[i].reward
		item_dict['post_date'] = requested_items[i].post_date
		responses = RequestResponse.objects.filter(item=requested_items[i])
		#print(responses.count())
		if responses.count() == 0:
			item_dict['no_response'] = True
		item_dict['responses'] = responses
		item_dict['description'] = requested_items[i].description
		context['items'].append(item_dict)


	#print(context['items'][1]['responses'][0].item.name)
	help_peer = RequestingItem.objects.all().exclude(borrower=request.user, )[:4]
	context['help_peer'] = help_peer
	return render(request, 'rent/my_requests.html', context)

@login_required
def view_profile(request, id):
	user = get_object_or_404(User, id=id)
	context = {"username": user.username,
				"firstname": user.first_name,
				"lastname":user.last_name}
	items = OfferingItem.objects.filter(lender=user)
	context['items'] = items


	return render(request, 'rent/profile.html', context)


def request_item(request, id):
	context={}
	item = OfferingItem.objects.get(id=id)
	user = request.user

	new_offer_response = OfferResponse(item=item, borrower=user)
	new_offer_response.save()
	print("request_saved")
	return redirect("search")

def make_transaction(request, item_id, borrower_id):
	print("here")
	context={}
	item = OfferingItem.objects.get(id=item_id)
	incoming_offer = OfferResponse.objects.get(item=item)
	lender=request.user
	borrower = User.objects.get(id=borrower_id)
	new_transaction = Transaction(lender=lender,borrower=borrower,is_offer=True,offer_item=item)
	new_transaction.save()
	return redirect("confirmedoffer")

def request_sent(request):
    context={}
    return render(request, 'rent/request_sent.html', context)

