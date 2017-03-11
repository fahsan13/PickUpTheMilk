from django.contrib import admin
from django.core.urlresolvers import reverse
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group
from MILK.models import Item, Transaction, UserProfile, GroupDetail, UserToGroup

class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'itemName', 'itemNeedsBought')

# Adapted from https://www.djangosnippets.org/snippets/1650/
# Using to display members of a group on the admin page
def Members(self):
    return ', '.join(['<a href="%s">%s</a>' % (reverse('admin:auth_user_change', args=(x.id,)), x.username) for x in self.user_set.all().order_by('username')])
Members.allow_tags = True

class GroupAdmin(GroupAdmin):
    list_display = ['name', Members]
    list_display_links = ['name']

#display doesn't work because formated string return type is not iterable, will need fixed
#class ItemToUser(admin.ModelAdmin):
#    list_display = ('userID')

#class UserProfile(admin.ModelAdmin):
#    list_display = ('balance')

# Adding user account ID to display in admin panel
UserAdmin.list_display = ('id','email', 'first_name', 'last_name', 'groups', 'date_joined', 'is_staff',)

admin.site.unregister(Group)
admin.site.register(Item, ItemAdmin)
admin.site.register(Transaction)
admin.site.register(UserProfile)
admin.site.register(Group, GroupAdmin)
admin.site.register(GroupDetail)
admin.site.register(UserToGroup)
