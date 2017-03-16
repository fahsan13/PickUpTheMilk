from django.conf.urls import url, include
from MILK import views

urlpatterns = [
    url(r'^$', views.home, name= 'home'),
    url(r'^sitemap/$', views.sitemap, name= 'sitemap'),
    url(r'^contact/$', views.contact, name= 'contact'),
    url(r'^about/$', views.about, name= 'about'),
    url(r'^create-group/$', views.creategroup, name= 'create-group'),
    url(r'^profile/(?P<username>[\w\-]+)/$', views.profilepage, name= 'profile'),
    url(r'^register_profile/$', views.register_profile, name='register_profile'),
    url(r'^group/(?P<groupname>[\w\-]+)/$', views.grouppage, name= 'group'),
    url(r'^recordpuchase/$', views.record_purchase, name= 'recordpurchase'),
    url(r'^needsbought/$', views.needsbought, name= 'needsbought'),
    url(r'^settle-up/(?P<groupname>[\w\-]+)/$', views.settleup, name= 'settle-up'),
    url(r'^resolvebalances/$', views.resolvebalances, name = 'resolvebalances'),
]
