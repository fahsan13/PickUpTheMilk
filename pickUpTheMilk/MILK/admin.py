from django.contrib import admin
from MILK.models import Item, ShoppingList, ItemToUser, UserToList, Transaction, UserProfile
# Register your models here.


admin.site.register(Item)
admin.site.register(ShoppingList)
admin.site.register(ItemToUser)
admin.site.register(UserToList)
admin.site.register(Transaction)
admin.site.register(UserProfile)
