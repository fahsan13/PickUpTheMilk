from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from MILK.models import Item, ShoppingList, ItemToUser, UserToList, Transaction, UserProfile
# Register your models here.

class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'itemName',)

class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'group')

#display doesn't work because formated string return type is not iterable, will need fixed
#class ItemToUser(admin.ModelAdmin):
#    list_display = ('userID')

#class UserProfile(admin.ModelAdmin):
#    list_display = ('balance')

# Adding user account ID to display in admin panel
UserAdmin.list_display = ('id','email', 'first_name', 'last_name', 'is_active', 'date_joined', 'is_staff',)

admin.site.register(Item, ItemAdmin)
admin.site.register(ShoppingList)
admin.site.register(ItemToUser)
admin.site.register(UserToList)
admin.site.register(Transaction)
admin.site.register(UserProfile)
