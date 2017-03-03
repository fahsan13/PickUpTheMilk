from django import forms
from django.contrib.auth.models import User, Group
from MILK.models import Item

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ('user', 'balance')

# Still in progress. Form to add item to database.
class itemForm(forms.ModelForm):
    itemName = forms.CharField(max_length=128,
                        help_text="Please enter the item name:")

    # Probably want this to be auto generated rather
    # than have the user enter an ID each time...
    itemID = forms.IntegerField(widget=forms.HiddenInput(),initial=0)
    class Meta:
        model = Item
        fields = ('itemName',)

class groupForm(forms.ModelForm):
    group = forms.CharField(max_length=128, help_text="Please enter the new group's name:")
    groupID = forms.IntegerField(widget=forms.HiddenInput(), initial = 1000)

    class Meta:
        model = Group
        fields = ('group',)
