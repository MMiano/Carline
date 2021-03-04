from django.conf.urls import url
from . import views

# Create your views here.

urlpatterns = [
	
	url(r'^$', views.home, name='home'),

	url(r'^login/$', views.login_user, name='login'),
	url(r'^logout/$', views.logout_user, name='logout'),
	url(r'^register/$', views.register_user, name='register'),
	url(r'^verify/$', views.verify_user, name='verify'),

	url(r'^request/$', views.request_product, name='request'),

	

	url(r'^view_profile/(?P<username>[\w-]+)/$', views.view_profile, name='view-profile'),
	url(r'^edit_profile/(?P<username>[\w-]+)/$', views.edit_profile, name='edit-profile'),

	url(r'^view_product/(?P<pk>\d+)/$', views.view_product, name='view-product'),
	url(r'^delete_product/(?P<pk>\d+)/$', views.delete_product, name='delete-product'),

	url(r'^add_product/$', views.add_product, name='add-product'),

	url(r'^owned_parts/$', views.owned_parts, name='owned-parts'),
	url(r'^owned_parts/confirm_request/$', views.confirm_request, name='confirm-request'),
	url(r'^owned_parts/revoke_request/$', views.revoke_request, name='revoke-request'),


	url(r'^requested_parts/$', views.requested_parts, name='requested-parts'),
	

	


]
