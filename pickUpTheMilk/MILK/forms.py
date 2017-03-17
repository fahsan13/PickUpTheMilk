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

# Used when a new group is created
class groupForm(forms.ModelForm):
    group = forms.CharField(max_length=128, help_text="Please enter the new group's name:")
    administrator = forms.ModelChoiceField(queryset= User.objects.all(), widget = forms.HiddenInput(), required = False)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(groupForm, self).__init__(*args, **kwargs)

    def clean_group(self):
        # .replace bit strips all whitespace from name entered.
        new_group, _ = Group.objects.get_or_create(name = self.cleaned_data.get('group').replace(" ", ""))
        return new_group

    def clean_administrator(self):
        return User.objects.get(id = self.user.id)

    def save(self, commit = True):
        # This is an attempt to override the save method to stop the group creating itself twice
        new_group_detail = GroupDetail.objects.create(group = self.cleaned_data.get('group'),administrator = self.cleaned_data.get('administrator'))

    class Meta:
        model = GroupDetail
        fields = ('group', 'administrator')

# Allows admin to add a user to a group...
class AddUser(forms.Form):
    user_to_add = forms.ModelChoiceField(queryset= User.objects.filter(groups=None))

# ... or remove a user from a group.
class RemoveUser(forms.Form):
    # Pass group into constructor as an argument, then filter user list
    # based on their group.
    def __init__(self, group, *args, **kwargs):
        super(RemoveUser, self).__init__(*args, **kwargs)
        self.fields['user_to_remove'] = forms.ChoiceField(
            choices=[(item.id, item) for item in User.objects.filter(groups=group)]
        )

# Allows users to track items purchased - form needs to be renamed to reflect this
class RecordPurchase(forms.ModelForm):
    # Filter items so can only see items that are on the too pick up list
    itemID = forms.ModelChoiceField(queryset=Item.objects.filter(itemNeedsBought = True))
    value = forms.DecimalField(required=True, min_value=0.01,
                                    help_text="Please enter price paid for item(s):")

    #should this be set to be the logged in user only?

    payeeID = forms.ModelChoiceField(queryset = User.objects.all())
    # purchaserID = forms.ModelChoiceField(queryset= User.objects.all(), widget = forms.HiddenInput(), required = False)

    class Meta:
        model = Transaction
        fields = ('value',)
        #this label thing doesn't work yet
        labels = { 'value': _('Fanny'),}
    # def clean_item(self):
        # id = Item.objects.get(id = self.item)

class needsBoughtForm(forms.Form):
    itemID = forms.ModelChoiceField(queryset=Item.objects.filter(itemNeedsBought = False))

    # class Meta:
    #     model = Item
    #     fields = ('itemNeedsBought',)

class ContactForm(forms.Form):
    name = forms.CharField(max_length=128)
    email = forms.CharField(max_length=128)
    comment = forms.CharField(widget=forms.Textarea)

    widgets = {'comment': forms.Textarea(attrs={'rows': 6,
                                               'cols': 100}),
               }
    class Meta:
        fields = ('name', 'email', 'comment')