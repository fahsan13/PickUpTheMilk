from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, Group

# Class for an item: tracks its name and whether or not it needs bought.
class Item(models.Model):

    itemName = models.CharField(max_length = 128, unique = True)
    itemNeedsBought = models.BooleanField(default = False)
    def __str__(self):
        return self.itemName
    def __unicode__(self):
        return self.itemName

# Extension to the default Django User model to add 'balance' field
class UserProfile(models.Model):
    # Line below links this extension to Django's User model
    user = models.OneToOneField(User)
    # Additional fields we want to track/store
    balance = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
    def __unicode__(self):
        return self.user.username
    def getUserID(self):
        return self.user.id

# Extension to the default Django Group model. Stores Administrator for a group.
class GroupDetail(models.Model):
    # Links this extension to the default Django Group model
    group = models.OneToOneField(Group)
    # Additional group details we want to store
    administrator = models.ForeignKey(User, null = True, related_name = 'the_group_creator')

    def __str__(self):
        return '{}'.format(self.group)
    def __unicode__(self):
        return '{}'.format(self.group)

class UserToGroup(models.Model):
    userID = models.OneToOneField(User)
    groupID = models.ForeignKey(Group)

    def __str__(self):
        return '{}'.format(self.id)
    def __unicode__(self):
        return '{}'.format(self.id)

class ShoppingList(models.Model):
    listID = models.IntegerField(default = 0, unique = True)
    # List name could be the address or whatever
    listName = models.CharField(max_length = 128, unique = False)
    user = models.ForeignKey(User, related_name ='ID')
    itemID = models.ForeignKey(Item)
    itemQuantity = models.IntegerField(default = 1)
    def __str__(self):
        return '{}'.format(self.user)
    def __unicode__(self):
        return '{}'.format(self.user)

class ItemToUser(models.Model):
    userID = models.ForeignKey(User)
    itemID = models.ForeignKey(Item)

    def __str__(self):
        return '{} , {}'.format(self.userID, self.itemID)
    def __unicode__(self):
        return '{} , {}'.format(self.userID, self.itemID)

# UserToList is an addition to ensure we could keep track of two separate
# groups with two separate lists (no overlap of users with multiple groups at
# this stage)
class UserToList(models.Model):
    userID = models.ForeignKey(User)
    listID = models.ForeignKey(ShoppingList)
    def __str__(self):
        return '{}'.format(self.userID)
    def __unicode__(self):
        return '{}'.format(self.userID)

# Dave removed all user names from the below table as these can be inferred
# from the IDs
class Transaction(models.Model):
    requestID = models.IntegerField(default = 0, unique = True)
    requestorID = models.ForeignKey(ItemToUser, related_name = 'requestorID')
    purchaserID = models.ForeignKey(User, related_name = 'purchaserID')
    payeeID = models.ForeignKey(User, related_name = 'payeeID')
    itemID = models.ForeignKey(Item, related_name = 'transactionItem')
    # Can handle items costing up to 9999.99
    value = models.DecimalField(max_digits=6, decimal_places=2)
    itemQuantity = models.IntegerField(default =1)
    # Date is useful for checking which items have recently been purchased
    DateandTime = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '{}'.self.requestID
    def __unicode__(self):
        return '{}'.self.requestID
