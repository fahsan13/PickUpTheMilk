from django.conf.urls import url
from MILK import views

urlpatterns = [
    url(r'^$', views.home, name= 'home'),
    url(r'^login/', views.user_login, name= 'login'),
    url(r'^register/', views.register, name= 'register'),
    url(r'^sitemap/', views.sitemap, name= 'sitemap'),
    url(r'^contact/', views.contact, name= 'contact'),
    url(r'^about/', views.about, name= 'about'),
    url(r'^create-group/', views.creategroup, name= 'creategroup'),
    url(r'^logout/', views.user_logout, name='logout'),

    # Work in progress
    url(r'^profileID=(?P<userID>[\w\-]+)/$', views.userprofile, name= 'profile'),

]
