from django.conf.urls import url, include
from MILK import views

urlpatterns = [
    url(r'^$', views.home, name= 'home'),
    url(r'^sitemap/$', views.sitemap, name= 'sitemap'),
    # url(r'^parralax/$', views.parralax, name= 'parralax'),
    url(r'^contact/$', views.contact, name= 'contact'),
    url(r'^about/$', views.about, name= 'about'),
    url(r'^create-group/$', views.creategroup, name= 'create-group'),
    url(r'^profile/(?P<username>[\w\-]+)/$', views.profilepage, name= 'profile'),
    url(r'^register_profile/$', views.register_profile, name='register_profile'),
    url(r'^group/(?P<groupname>[\w\-]+)/$', views.grouppage, name= 'group'),
    # url(r'^recordpuchase/$', views.record_purchase, name= 'recordpurchase'),
    url(r'^needsbought/$', views.needsbought, name= 'needsbought'),
    url(r'^settle-up/(?P<groupname>[\w\-]+)/$', views.settleup, name= 'settle-up'),
    url(r'^suggest_item/$', views.suggest_item, name='suggest_item'),
    url(r'^suggest_add_item/$', views.suggest_add_item, name='suggest_add_item'),
    url(r'^item_needs_bought/$', views.item_needs_bought, name='item_needs_bought'),
    url(r'^resolve_balances/$', views.resolve_balances, name='resolve_balances'),
    url(r'^average_balances/$', views.average_balances, name='average_balances'),

]
