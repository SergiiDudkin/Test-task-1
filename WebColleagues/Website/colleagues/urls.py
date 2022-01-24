from django.urls import re_path
from colleagues import views

urlpatterns = [
	re_path(r'^$', views.home, name='home'),
	re_path(r'^home/$', views.home, name='home'),
	re_path(r'^signup/$', views.signup, name='signup'),
	re_path(r'^login/$', views.login_, name='login'),
	re_path(r'^logout/$', views.logout_, name='logout'),
	re_path(r'^profile/$', views.my_account, name='profile'),
	re_path(r'^set_benefits/(?P<pk>\d+)/$', views.set_benefits, name='set_benefits'),
	re_path(r'^save_benefits/(?P<pk>\d+)/$', views.save_benefits, name='save_benefits'),
	re_path(r'^upload_img/$', views.upload_img, name='upload_img'),
]
