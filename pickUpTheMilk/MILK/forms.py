from django import forms
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

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(itemForm, self).__init__(*args, **kwargs)

    # def clean_addedby(self):
    #     user = User.objects.get(id = self.user.id)
    #     return user
    #
    # def clean_groupBuying(self):
    #     group = User.objects.get(groups = self.group)
    #     return group

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

# Allows admin to add a user to a group
# TO-DO - any way to filter so only shows users who have no
# group?
class AddUser(forms.Form):
    user = forms.ModelChoiceField(queryset= User.objects.filter(groups=None))

# allows item to be bought
class BuyItem(forms.Form):
    id = forms.ModelChoiceField(queryset=Item.objects.all())
    purchasePrice = forms.FloatField(required=True, min_value=0.01,
                                    help_text="Please enter price paid for item(s):")
    numPurchased = forms.IntegerField(required=True, min_value=1,
                                     help_text="Please enter price paid for item(s):")
    purchaserID = forms.ModelChoiceField(queryset= User.objects.all(), widget = forms.HiddenInput(), required = False)

    class Meta:
        model = Transaction
        fields = ('purchaserID', 'id', 'purchasePrice')
    # def clean_item(self):
    # id = Item.objects.get(id = self.item)
