from django.contrib import admin
from MILK.models import Item, User, ShoppingList, ItemToUser, UserToList, Transaction 
# Register your models here.


admin.site.register(Item)
admin.site.register(User)
admin.site.register(ShoppingList)
admin.site.register(ItemToUser)
admin.site.register(UserToList)
admin.site.register(Transaction)
