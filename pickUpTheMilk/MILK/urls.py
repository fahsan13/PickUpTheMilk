from django.conf.urls import url
from MILK import views

urlpatterns = [
    url(r'^$', views.home, name= 'home'),
    url(r'^login/', views.login, name= 'login'),
    url(r'^register/', views.register, name= 'register'),
    url(r'^sitemap/', views.sitemap, name= 'sitemap'),
    url(r'^contact/', views.contact, name= 'contact'),
    url(r'^about/', views.about, name= 'about'),
    url(r'^create-group/', views.creategroup, name= 'sitemap'),

    # Work in progress
    # url(r'^profileID=(?P<profileID>[\w\-]+)/$', views.profile, name= 'profile'),

]
