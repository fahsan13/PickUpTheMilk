from django import forms
from django.contrib.auth.models import User, Group
from MILK.models import Item, UserProfile, GroupDetail

# Form displayed in Step 2 of user registration process
class UserProfileForm(forms.ModelForm):
    balance = forms.DecimalField(widget=forms.HiddenInput(),initial=0)
    picture = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ('balance', 'picture')

# Form to add an item to database.
class itemForm(forms.ModelForm):
    itemName = forms.CharField(max_length=128,
                        help_text="Please enter the item name:")

    class Meta:
        model = Item
        fields = ('itemName',)

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
        model = Group
        fields = ('group', 'administrator')
