from django.conf.urls import url, include
from MILK import views

urlpatterns = [
    url(r'^$', views.home, name= 'home'),
    url(r'^sitemap/$', views.sitemap, name= 'sitemap'),
    url(r'^contact/$', views.contact, name= 'contact'),
    url(r'^about/$', views.about, name= 'about'),
    # url(r'^register_profile/$', views.register_profile, name='register_profile'),
    url(r'^profile/(?P<userprofile_user_slug>[\w\-]+)/$', views.profilepage, name= 'profile'),
    url(r'^group/(?P<groupname>[\w\-]+)/$', views.grouppage, name= 'group'),

    # URLs below are for AJAX related functions.
    url(r'^suggest_add_item/$', views.suggest_add_item, name='suggest_add_item'),
    url(r'^user_search/$', views.user_search, name='user_search'),
    url(r'^add_user/$', views.add_user, name='add_user'),
    url(r'^item_needs_bought/$', views.item_needs_bought, name='item_needs_bought'),
    url(r'^resolve_balances/$', views.resolve_balances, name='resolve_balances'),
    url(r'^average_balances/$', views.average_balances, name='average_balances'),
]
