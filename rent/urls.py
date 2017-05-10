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
	url(r'^add_new$', rent_views.add_new, name='add_new'),
	url(r'^submit_offer$', rent_views.submit_offer, name='submit_offer'),
	url(r'^offer_item$', rent_views.offer_item, name='offer_item'),
	# url(r'^login$', auth_views.login, {'template_name':'rent/login_temp.html'}, name='login'),
 	# url(r'^logout$', auth_views.logout_then_login, name="logout"),
    # url(r'^register$', rent_views.register, name="register"),
    url(r'^login$', rent_views.login_modal, name='login'),
    url(r'^login_authenticate$', rent_views.login_authenticate, name='login_authenticate'),
    url(r'^register$', rent_views.register, name="register"),
    url(r'^logout$', rent_views.logout_user, name='logout'),
    url(r'^my_requests$', rent_views.my_requests, name="my_requests"),
    url(r'^item_photo/(?P<id>\S+)$', rent_views.get_item_photo, name="get_item_photo"),
    url(r'^profile/(?P<id>\d+)$', rent_views.view_profile, name="profile"),
    url(r'^request_item/(?P<id>\d+)$', rent_views.request_item, name="request_item")
]