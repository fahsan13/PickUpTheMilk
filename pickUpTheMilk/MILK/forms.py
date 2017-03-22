import string, sys, unicodedata
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from MILK.models import Item, UserProfile, GroupDetail, Transaction

# Form displayed in Step 2 of user registration process
class UserProfileForm(forms.ModelForm):
    balance = forms.DecimalField(widget=forms.HiddenInput(),initial=0)
    picture = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ('balance', 'picture')

# Form to add an item to database.
class itemForm(forms.ModelForm):
    itemName = forms.CharField(max_length=128, help_text="Please enter the item name:")
    addedby = forms.ModelChoiceField(queryset= User.objects.all(), widget = forms.HiddenInput(), required = False)
    groupBuying = forms.ModelChoiceField(queryset= Group.objects.all(), widget = forms.HiddenInput(), required = False)

    class Meta:
        model = Item
        # fields = ('itemName', 'addedby', 'groupBuying')
        fields = ('itemName', 'addedby', 'groupBuying')

# Form for AJAX autocomplete of items to be added to a group's list
class autoItemForm(forms.ModelForm):
    itemName = forms.CharField(max_length=128, help_text="Please enter the item name:")
    addedby = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput(), required=False)
    groupBuying = forms.ModelChoiceField(queryset=Group.objects.all(), widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Item
        fields = ('itemName', 'addedby', 'groupBuying')

# Used when a new group is created
class groupForm(forms.ModelForm):
    group = forms.CharField(max_length=128, help_text="Please enter the new group's name:")
    administrator = forms.ModelChoiceField(queryset= User.objects.all(), widget = forms.HiddenInput(), required = False)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(groupForm, self).__init__(*args, **kwargs)

    def clean_group(self):
        # '.replace' section strips all whitespace from name entered.
        name = self.cleaned_data.get('group').replace(" ", "")
        # Strip punctuation; call helper method
        cleaned_name = remove_punctuation(name)
        new_group, _ = Group.objects.get_or_create(name = cleaned_name)
        return new_group

    def clean_administrator(self):
        return User.objects.get(id = self.user.id)

    def save(self, commit = True):
        # This is an attempt to override the save method to stop the group creating itself twice
        new_group_detail = GroupDetail.objects.create(group = self.cleaned_data.get('group'),administrator = self.cleaned_data.get('administrator'))

    class Meta:
        model = GroupDetail
        fields = ('group', 'administrator')

# Allows user remove a user from a group.
class RemoveUser(forms.Form):
    # Pass group into constructor as an argument, then filter user list
    # based on their group.
    def __init__(self, group, *args, **kwargs):
        super(RemoveUser, self).__init__(*args, **kwargs)
        self.fields['user_to_remove'] = forms.ChoiceField(
            choices=[(item.id, item) for item in User.objects.filter(groups=group)]

        )

# Allows users to track items purchased.
class RecordPurchase(forms.ModelForm):
    # Filter items so can only see items that are on the 'to pick up' list
    #itemID = forms.ModelChoiceField(queryset=Item.objects.filter(itemNeedsBought = True))


    def __init__(self, group, *args, **kwargs):
        super(RecordPurchase, self).__init__(*args, **kwargs)
        self.fields['itemID'] = forms.ChoiceField(
            choices=[(item, item) for item in Item.objects.filter(itemNeedsBought=True).filter(groupBuying=group)]

        )
    value = forms.DecimalField(required=True, min_value=0.01,
                               help_text="Please enter price paid for item(s):")

    payeeID = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Transaction
        fields = ('value',)

# Form to change the 'needs bought' status of an item.
class needsBoughtForm(forms.Form):
    # itemID = forms.ModelChoiceField(queryset=Item.objects.filter(itemNeedsBought = False))
    def __init__(self, group, *args, **kwargs):
        super(needsBoughtForm, self).__init__(*args, **kwargs)
        self.fields['itemID'] = forms.ChoiceField(
            choices =[(item, item) for item in Item.objects.filter(itemNeedsBought = False).filter(groupBuying = group)]
            )

# Form that is displayed on 'Contact Us' page.
class ContactForm(forms.Form):
    name = forms.CharField(max_length=128)
    email = forms.CharField(max_length=128)
    comment = forms.CharField(widget=forms.Textarea)

    widgets = {'comment': forms.Textarea(attrs={'rows': 6,
                                               'cols': 100}),
               }
    class Meta:
        fields = ('name', 'email', 'comment')

# Form to allow user to upload new profile picture - don't want to reset their balance!
class ProfilePictureForm(forms.ModelForm):
    picture = forms.ImageField(required=False, help_text="Upload a new profile picture!")

    class Meta:
        model = UserProfile
        fields = ('picture',)

# Helper method to strip punctuation from a string.
# Adapted from: http://stackoverflow.com/questions/11066400/remove-punctuation-from-unicode-formatted-strings
def remove_punctuation(text):
    tbl = dict.fromkeys(i for i in xrange(sys.maxunicode) if unicodedata.category(unichr(i)).startswith('P'))
    return text.translate(tbl)
