from django.conf.urls import url, include
from MILK import views

urlpatterns = [
    url(r'^$', views.home, name= 'home'),
    url(r'^sitemap/$', views.sitemap, name= 'sitemap'),
    url(r'^contact/$', views.contact, name= 'contact'),
    url(r'^about/$', views.about, name= 'about'),
    url(r'^create-group/$', views.creategroup, name= 'create-group'),
    url(r'^profile/$', views.userprofile, name= 'profile'),
    url(r'^register_profile/$', views.register_profile, name='register_profile'),



    # Work in progress
    # url(r'^profileID=(?P<userID>[\w\-]+)/', views.userprofile, name= 'profile'),
    # url(r'^profileID=(?P<userID>^\d*[1-9]\d*$)/', views.userprofile, name= 'profile'),
]
