from django.conf.urls import url, include
from MILK import views

urlpatterns = [
    url(r'^$', views.home, name= 'home'),
    url(r'^sitemap/', views.sitemap, name= 'sitemap'),
    url(r'^contact/', views.contact, name= 'contact'),
    url(r'^about/', views.about, name= 'about'),
    url(r'^create-group/', views.creategroup, name= 'creategroup'),
    url(r'^accounts/', include('registration.backends.simple.urls')),



    # Work in progress
    url(r'^profileID=(?P<userID>[\w\-]+)/$', views.userprofile, name= 'profile'),

    url(r'^additem/', views.additem, name= 'additem'),

]
