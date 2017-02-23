from __future__ import unicode_literals

from django.db import models

# Create your models here.


class User(models.Model):
    userID = models.IntegerField(max_length = 16, unique = True)
    userName = models.CharField(max_length = 128, unique = False)
    Balance = models.DecimalField(max_digits=6, decimal_places=2)
    listID = models.ForeignKey(ShoppingList)

class ItemToUser(models.Model):
    userID = models.ForeignKey(User)
    itemID = models.ForeignKey(Item)


class Item(models.Model):
    itemID = models.IntegerField(max_length = 16, unique = True)
    itemName = models.CharField(max_length = 128, unique = True)

##UserToList is an addition to ensure we could keep track of two separate
##groups with two separate lists (no overlap of users with multiple groups at
## this stage)
class UserToList
    userID = models.ForeignKey(User)
    listID = models.ForeignKey(ShoppingList)

class ShoppingList(models.Model):
    listID = models.IntegerField(max_length = 16, unique = True)
    #list name could be the address or whatever
    listName = models.CharField(max_length = 128, unique = False)
    userID = models.ForeignKey(User)
    userName = models.ForeignKey(User)
    itemID = models.ForeignKey(Item)
    itemName = models.ForeignKey(Item)
    itemQuantity = models.IntegerField(default = 1)

# have removed all user names from the below table as these can be inferred
# from the ids 
class Transaction(models.Model):
    requestID = models.ForeignKey(ShoppingList)
    requestorID = models.ForeignKey(ItemToUser)
    purchaserID = models.ForeignKey(User)
    itemID = models.ForeignKey(Item)
    # can handle items costing up to £9999.99
    Value = models.DecimalField(max_digits=6, decimal_places=2)
    itemQuantity = models.IntegerField(default =1)
    # date is useful for checking which items have recently been purchased
    DateandTime = DateTimeField(auto_now=False, auto_now_add=False, **options)
