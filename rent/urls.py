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

]