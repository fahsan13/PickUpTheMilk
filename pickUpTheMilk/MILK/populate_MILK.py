import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page

def populate():
# First, we will create lists of dictionaries containing the pages
# we want to add into each category.
# Then we will create a dictionary of dictionaries for our categories.
# This might seem a little bit confusing, but it allows us to iterate
# through each data structure, and add the data to our models.

user = [
    {"userID" : "9001", "userName" : "Lance Steel", "Balance" : 10.50 },
    {"userID" : "9002", "userName" : "Samantha Cowlove", "Balance": 5.00},
    {"userID" : "9003", "userName" : "Paul TheOtherGuy", "Balance": -30.20}
    ]














django_pages = [
    {"title":"Official Django Tutorial",
    "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial01/"},
27 {"title":"Django Rocks",
28 "url":"http://www.djangorocks.com/"},
29 {"title":"How to Tango with Django",
30 "url":"http://www.tangowithdjango.com/"} ]
31
32 other_pages = [
33 {"title":"Bottle",
34 "url":"http://bottlepy.org/docs/dev/"},
35 {"title":"Flask",
36 "url":"http://flask.pocoo.org"} ]
37
38 cats = { }
mhgjhg
51 for cat, cat_data in cats.items():
52 c = add_cat(cat)
53 for p in cat_data["pages"]:
54 add_page(c, p["title"], p["url"])
55
56 # Print out the categories we have added.
57 for c in Category.objects.all():
58 for p in Page.objects.filter(category=c):
59 print("- {0} - {1}".format(str(c), str(p)))
60
61 def add_page(cat, title, url, views=0):
62 p = Page.objects.get_or_create(category=cat, title=title)[0]
63 p.url=url
64 p.views=views
65 p.save()
66 return p
67
68 def add_cat(name):
69 c = Category.objects.get_or_create(name=name)[0]
70 c.save()
71 return c
72
73 # Start execution here!
74 if __name__ == '__main__':
75 print("Starting Rango population script...")
76 populate()
