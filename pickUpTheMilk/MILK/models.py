from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Item(models.Model):
    itemID = models.IntegerField(default = 0, unique = True)
    itemName = models.CharField(max_length = 128, unique = True)

    def __str__(self):
        return self.itemID
    def __unicode__(self):
        return self.itemID

# Extension to the default Django User model to add 'balance' field
class UserProfile(models.Model):
    # Line below links this extension to the base user model
    user = models.OneToOneField(User)
    balance = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.user.username
    def __unicode__(self):
        return self.user.username
        # Do we need to create an ID field?

class ShoppingList(models.Model):
    listID = models.IntegerField(default = 0, unique = True)
    #list name could be the address or whatever
    listName = models.CharField(max_length = 128, unique = False)
    user = models.ForeignKey(User, related_name ='ID')
    itemID = models.ForeignKey(Item)
    itemQuantity = models.IntegerField(default = 1)
    def __str__(self):
        return self.listID
    def __unicode__(self):
        return self.listID

class ItemToUser(models.Model):
    userID = models.ForeignKey(User)
    itemID = models.ForeignKey(Item)
    def __str__(self):
        return self.userID
    def __unicode__(self):
        return self.userID


##UserToList is an addition to ensure we could keep track of two separate
##groups with two separate lists (no overlap of users with multiple groups at
## this stage)
class UserToList(models.Model):
    userID = models.ForeignKey(User)
    listID = models.ForeignKey(ShoppingList)
    def __str__(self):
        return self.userID
    def __unicode__(self):
        return self.userID

# have removed all user names from the below table as these can be inferred
# from the ids
class Transaction(models.Model):
    requestID = models.IntegerField(default = 0, unique = True)
    requestorID = models.ForeignKey(ItemToUser, related_name = 'requestorID')
    purchaserID = models.ForeignKey(User, related_name = 'purchaserID')
    payeeID = models.ForeignKey(User, related_name = 'payeeID')
    itemID = models.ForeignKey(Item, related_name = 'transactionItem')
    # can handle items costing up to 9999.99
    value = models.DecimalField(max_digits=6, decimal_places=2)
    itemQuantity = models.IntegerField(default =1)
    # date is useful for checking which items have recently been purchased
    DateandTime = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.requestID
    def __unicode__(self):
        return self.requestID
