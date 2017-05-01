from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from rent import views as rent_views

urlpatterns = [
	url(r'^$', rent_views.home, name='home'),
	url(r'^search$', rent_views.search, name='search'),
	url(r'^search_ajax$', rent_views.search_ajax, name='search_ajax'),
	url(r'^userpicture/(?P<id>\S+)$', rent_views.get_user_photo, name='userpicture'),
	url(r'^userpicture$', rent_views.get_user_photo, name='userpicture'),
	url(r'^send_request_ajax$', rent_views.send_request_ajax, name='send_request_ajax'),
	url(r'^incomingoffer$', rent_views.incomingoffer, name='incomingoffer'),
	url(r'^confirmedoffer$', rent_views.confirmedoffer, name='confirmedoffer'),
	url(r'^myalloffer$', rent_views.myalloffer, name='myalloffer'),
	url(r'^help_peer_detail/(?P<id>\S+)$', rent_views.help_peer_detail, name='help_peer_detail'),
]