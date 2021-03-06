from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Sum
import json
from MILK.models import User, UserProfile, Group, GroupDetail, Item
from MILK.forms import itemForm, groupForm, UserProfileForm, RemoveUser, RecordPurchase, needsBoughtForm, ContactForm, ProfilePictureForm, CustomRegistration
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from registration.backends.simple.views import RegistrationView

# Create a new class that redirects the user to the index page, if successful at logging
class MyRegistrationView(RegistrationView):

    def get_success_url(self, user):
        return '/'

# View for the home page of the site.
def home(request):

    user=request.user

    item_list = Item.objects.order_by('id')
    app_url = request.path

    if request.user.is_authenticated():

        rsp_template = 'MILK/home.html'
        # form to record the purchase of an item
        purchase_form = recPurchHelper(request)
        # form to update the list of items needed
        update_form = updateListHelper(request)

        userprofile = getUserProfile(request)
        # Form to allow user to add a new item to the shopping list
        newitem_form = newItemForm(request,user)

        # For form that allows user to create a group
        # Will only dispaly if user is not a member of a group
        group_add_form = createGroupForm(request)

        context_dict = {'Items': item_list,
                        'app_url': app_url,
                        'purchaseform': purchase_form,
                        'updateform': update_form,
                        'userprofile': userprofile,
                        'groupform':group_add_form,
                        'new_item_form':newitem_form,}

    else:
        # User not authenticated; show them parallax version
        rsp_template = 'MILK/parallax.html'
        context_dict = {'app_url': app_url}

    response = render(request, rsp_template, context_dict)
    return response

# handles recording purchase form process
def recPurchHelper(request):
    # Get user's group
    user = request.user
    # Handles error in case of a user without a UserProfile (superuser) accessing the home page.
    # Get or create means that if it doesn't exist, we make one!
    userprofile = UserProfile.objects.get_or_create(user=request.user)[0]
    group = user.groups.all().first()

    form = RecordPurchase(group)

    if request.method == 'POST' and 'purchaseButton' in request.POST:

        form = RecordPurchase(group,request.POST)

        if form.is_valid():
            purchase = form.save(commit=False)

            # Gets item purchased
            item_purchased = form.cleaned_data['itemID']

            # Get cost of transaction entered by user from form
            item_cost = form.cleaned_data['value']

            # Get this user's userprofile, where their balance is stored
            userprofile = UserProfile.objects.get_or_create(user=request.user)[0]

            # Gets item object to allow toggling of needsbought booleanfield
            toggle_item_bought = Item.objects.get(itemName=item_purchased, groupBuying=group)

            # Reflect this on user's balance
            userprofile.balance += item_cost

            # Sets items needs bought status to false, for item model
            toggle_item_bought.itemNeedsBought = False

            # Updates the transaction model
            purchase.payeeID = request.user
            purchase.itemID = toggle_item_bought

            # Saves changes
            userprofile.save()
            toggle_item_bought.save()
            purchase.save()
            # calls form again so that it is set as blank for next purchase
            form = RecordPurchase(group)
        else:
            print(form.errors)
    return form

# Helper method to handle the form for when user adds new item to their full list.
def updateListHelper(request):

    # Get user's group
    user = request.user
    group = user.groups.all().first()

    # Imports form used to display items which aren't currently marked as needing to be bought
    form = needsBoughtForm(group)

    if request.method == 'POST' and "pickUpButton" in request.POST:
        form = needsBoughtForm(group, request.POST)

        if form.is_valid():
            # Gets item name for item to be bought
            name = form.cleaned_data['itemID']

            # Get the correct item object by filtering based on 'name' and group
            item_needing_bought = Item.objects.get(itemName = name, groupBuying = group)

            # Sets items 'needs bought' status to false, for item model
            item_needing_bought.itemNeedsBought = True

            # Saves change
            item_needing_bought.save()

            # Refresh the form
            form = needsBoughtForm(group)
        else:
             print(form.errors)
    return form

# View for sitemap
def sitemap(request):

    app_url = request.path

    user = request.user
    # Get the user profile so profile sidebar can render balance.
    user_profile = getUserProfile(request)

    group = None
    if user.groups.all().first() != None:
        group = user.groups.all().first()

    context_dict = {'app_url': app_url,
                    'user':user,
                    'userprofile':user_profile,
                    'group':group}

    response = render(request, 'MILK/sitemap.html', context_dict)
    return response

# View for contact page
def contact(request):

    # Gets the current URL - used for CSS
    app_url = request.path

    # Get the user profile so profile sidebar can render balance.
    user_profile = getUserProfile(request)

    # Form to be displayed for users to contact the site.
    form = ContactForm()

    context_dict = {'app_url': app_url, 'form':form, 'userprofile':user_profile}

    return render(request, 'MILK/contact.html', context_dict)

#  View for the about page
def about(request):

    # Gets the current URL - used for CSS
    app_url = request.path

    # Get the user profile so profile sidebar can render balance.
    user_profile = getUserProfile(request)

    return render(request, 'MILK/about.html', {'app_url': app_url, 'userprofile':user_profile})


# Helper method for create group form
def createGroupForm(request):

    form = groupForm(request.POST)

    # Get currently logged in user.
    user=request.user
    # Get their user profile
    user_profile = getUserProfile(request)

    if request.method == 'POST':
        form = groupForm(user, request.POST)
        if form.is_valid():
            # Save the group
            group=form.save(commit=True)
            # Get group name from form; field within form containing name is 'group'!
            groupname = form.cleaned_data['group']
            # Add the user to this newly created group
            user.groups.add(groupname)
            print(group)

            # Redirect user to their profile if group succcessfully created
            return redirect('profile', user_profile.slug)
        else:
            print(form.errors)

    return(form)

# View for a user's profile
@login_required
def profilepage(request, userprofile_user_slug):

    try:
        # May want to view another user's profile!
        userprofile = UserProfile.objects.get(slug=userprofile_user_slug)

        # Retrieve UserProfile extension (containing balance/picture).
        # We will then pass this to profile.html
        user = userprofile.user

        # User should only functionally have one group. If
        # it exists, we select it. If it doesn't, form won't
        # be rendered anyway.
        if user.groups.all().first() != None:
            group = user.groups.all().first()

    except User.DoesNotExist:
        return redirect('home')

    # Form to add a new item (calls helper method)
    new_item = newItemForm(request, user)
    # Form to create a new group (calls helper method)
    group_add_form = createGroupForm(request)

    picture_form = ProfilePictureForm({'picture': userprofile.picture})

    # Allow user to upload new picture. New form used as we don't want to overwrite balance.
    if request.method == 'POST' and "picturebutton" in request.POST:
        picture_form = ProfilePictureForm(request.POST, request.FILES, instance = userprofile)

        if picture_form.is_valid():
            picture_form.save(commit=True)
            return redirect('profile', userprofile.slug)
        else:
            print(picture_form.errors)

    # Get items so we can display on user's page
    item_list = Item.objects.order_by('id')

    # Used for CSS purposes
    app_url = '/profile/'

    context_dict = {'Items': item_list,
                    'new_item': new_item,
                    'pictureform':picture_form,
                    'groupform':group_add_form,
                    'selecteduser':user,
                    'userprofile': userprofile,
                    'app_url':app_url,
                    'new_item':new_item,}

    response = render(request, 'MILK/userprofile.html', context_dict)
    return response

# View for communal group page
@login_required
def grouppage(request, groupname):

    # Get current user
    user=request.user
    # Get all members of the group
    groupmembers = User.objects.filter(groups__name=groupname)

    user_profile = getUserProfile(request)

    try:
        # No idea why this is working; change groupname
        # reference on left and it breaks :/
        groupname = Group.objects.get(name=groupname)
        groupdetail = GroupDetail.objects.get(group=groupname)
    except Group.DoesNotExist:
        return redirect('home')

    # Not a POST, so just render empty form
    remove_form = RemoveUser(groupname)

    # If admin presses button to remove user, instead do the following:
    if request.method == 'POST' and 'removeuserbutton' in request.POST:
        remove_form = RemoveUser(groupname, request.POST)

        # Deal with remove_form
        if remove_form.is_valid():
            currentuser =request.user
            selecteduserID = remove_form.cleaned_data['user_to_remove']
            currentuserID = currentuser.id
            # selecteduser = User.objects.get(id=selecteduserID)

            # cast to strings for comparision purposes, probably would know a better with some python lectures
            valueCID = int(currentuserID)
            valueSID = int(selecteduserID)

            #user cannot remove themselves from a group
            if valueCID != valueSID:
                # Filter user based on their ID
                selecteduser = User.objects.get(id=selecteduserID)
                selecteduser.groups.remove(groupname)

                print("User successfully removed!")
                return redirect('group', groupname)
            else:

                return redirect('group', groupname)
        else:
            print(remove_form.errors)

    # Used for nav bar - makes its corresponding section white when we're on the group page.
    app_url = '/group/'

    context_dict = {'currentgroup':groupname,
                    'groupdetail':groupdetail,
                    'user':user,
                    'removeform':remove_form,
                    'members':groupmembers,
                    'userprofile':user_profile,
                    'app_url':app_url}

    response = render(request, 'MILK/grouppage.html', context_dict)
    return response

# Method which auto-suggests an item to be added to the 'Items To Pick Up' list
def suggest_add_item(request):
    item_list = []
    starts_with = ''

    if request.method == 'GET':
        starts_with = request.GET['suggestion']
        user = request.user
        usergroup = user.groups.all().first()

        print starts_with

    item_list = get_add_item_list(usergroup ,4, starts_with)
    print item_list

    return render(request, 'milk/add_items.html', {'Items': item_list})

# Helper method for 'suggest_add_item'
def get_add_item_list(usergroup, max_results=0, starts_with=''):
    item_list = []
    if starts_with:
        # Use the user's group to filter and only show item from their group shopping list
        item_list = Item.objects.filter(itemName__istartswith=starts_with, itemNeedsBought = False, groupBuying = usergroup )

    if max_results > 0:
        if len(item_list) > max_results:
            item_list = item_list[:max_results]
    print item_list
    return item_list

# Ajax to search for a user to add
def user_search(request):
    user_list = []
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']
        user = request.user

        print starts_with
    user_list = get_user_list(4, starts_with)
    print user_list

    return render(request, 'MILK/user_search.html', {'Users': user_list})

# Helper method to search for users.
def get_user_list(max_results=0, starts_with=''):
    user_list = []
    if starts_with:
        # Search for users who don't have a group
        user_list = User.objects.filter(username__istartswith=starts_with, groups = None,)

    if max_results > 0:
        if len(user_list) > max_results:
            user_list = user_list[:max_results]
    print user_list
    return user_list

# Method using AJAX to add a user to a group
def add_user(request):
    user_to_add = None
    if request.method == 'GET':
        username_to_add = request.GET['user_adding']

        # Get administrator's group - they are logged in!
        user = request.user
        usergroup = user.groups.all().first()
        # Get the actual user object for the user to add
        user_to_add = User.objects.get(username = username_to_add)
        # Add this usee to the admin's group
        user_to_add.groups.add(usergroup)
        # Save
        user_to_add.save()

        return HttpResponse(True)

# View to take an item ID from an AJAX query so we can set items needsbought status to true.
def item_needs_bought(request):
    item_id = None
    if request.method == 'GET':

        item_id = request.GET['item_adding']

        # Get the item to add using item_id to filter.
        item_to_add = Item.objects.get(itemName=item_id)
        if item_to_add:
            item_to_add.itemNeedsBought = True
            item_to_add.save()

        item_list = []

        # Get user's group
        user = request.user
        usergroup = user.groups.all().first()

        # Use the user's group in here to filter and only show items from their shopping list
        item_list = Item.objects.filter(itemNeedsBought = True, groupBuying = usergroup )

    return render(request, 'MILK/needsBoughtList.html', {'Items': item_list})

# View using AJAX to resolve group balances to 0.
@login_required
def resolve_balances(request):
    current_group = request.GET['current_group']
    print current_group
    group_members = User.objects.filter(groups__name=current_group)
    zero_balance = 0
    print group_members
    for v in group_members:
        userTo0 = v
        userprofileto0 = UserProfile.objects.get(user=userTo0)
        print userTo0
        print userprofileto0.balance
        userprofileto0.balance = zero_balance
        print userprofileto0.balance
        userprofileto0.save()
    response = render(request, 'MILK/settled_balances.html', {'members': group_members,})
    return response

# Method to work out the money owed by each group member
# Used in settling balances calculations.
def average_balances(request):

    current_group = request.GET['current_group']
    groupmembers = User.objects.filter(groups__name=current_group).order_by()
    total = 0
    nummembers = 0
    output = []
    # Gets user name = v in groupmembers
    for v in groupmembers:
        # Iterate through the members of a group getting matching user profiles
        user_profile = UserProfile.objects.get(user=v)
        # Get the balance and round to two decimal places
        money = user_profile.balance
        money = round(money, 2)
        # Track total ammount spent by a group and number of group members
        total = total + money
        nummembers = nummembers + 1

    # Determine average owed
    average = total / nummembers
    average = round(average, 2)
    final_balance = 0
    for v in groupmembers:
        user_profile = UserProfile.objects.get(user=v)
        user = user_profile.user
        user_name = user.username
        # Get user spending
        user_balance = user_profile.balance
        # Cast to float prior to calculations
        user_float = float(user_balance)
        # What each user owes is current balance minus average
        finalbalance = user_float - average

        # Handle whether user is owed or owes money since last settlement
        if finalbalance < 0:
            finalbalance = abs(finalbalance)
            print "abs:"
            print finalbalance
            finalbalance = round(finalbalance, 2)
            finalbalstring = str.format('%.2f' % finalbalance)
            useroutput = user_name + " owes: " + unichr(163) + finalbalstring
            output.append(useroutput)
        else:
            finalbalance = round(finalbalance, 2)
            finalbalstring = str.format('%.2f' % finalbalance)
            useroutput = user_name + " is owed: " + unichr(163) + finalbalstring
            output.append(useroutput)
        final_balance = 0
    response = render(request, 'MILK/averaged_balances.html', {'user_balances': output})
    return (response)

# Helper method to get currently logged in user's userprofile
def getUserProfile(request):

    user = request.user

    if user.is_authenticated():
        user_profile = UserProfile.objects.get(user = user)
        return user_profile


# New item form helper method for template
def newItemForm(request,user):
    form = itemForm()
    user_profile = UserProfile.objects.get(user=user)
    group = user.groups.all().first()
        # Deal with itemForm
    if request.method == 'POST' and "itembutton" in request.POST:
        form = itemForm(request.POST)

        if form.is_valid():
            item=form.save(commit=False)
            # Assign the user who added the item and the group it belongs to
            item_name = form.cleaned_data['itemName']

            # The lines below check to see if an item with this name already exists
            # for this group. If it does, we don't save it as a new item. If it
            # doesn't, we add it as a new item. This means that 2 groups can have
            # an item with the same name, but a single group can't have the same item
            # twice.
            try:
                item_check = Item.objects.get(itemName = item_name, groupBuying = group)
                print "Error! Item already exists."
            except Item.DoesNotExist:
                item.addedby = user
                item.groupBuying = group
                item.save()
                print "Item successfully added"
        else:
            print(form.errors)
    return form
