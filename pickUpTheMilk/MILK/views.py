from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Sum
import json
from MILK.models import User, UserProfile, Group, GroupDetail, Item
from MILK.forms import itemForm, groupForm, UserProfileForm, AddUser, RemoveUser, RecordPurchase, needsBoughtForm, ContactForm, ProfilePictureForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# View for second page in 2-step registration process. Required as we're
# using registration-redux package and still want to populate the UserProfile
# fields --(initial) balance and picture-- when the user registers.
@login_required
def register_profile(request):
    form = UserProfileForm()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            return redirect('home')
        else:
            print(form.errors)
    context_dict = {'form':form}
    return render(request, 'MILK/profile_registration.html', context_dict)

# View for the home page of the site.
def home(request):

    user=request.user

    if user.groups.all().first() != None:
        group = user.groups.all().first()

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
    form = RecordPurchase()
    # selecteduser = request.user

    if request.method == 'POST' and 'purchaseButton' in request.POST:
        form = RecordPurchase(request.POST)

        if form.is_valid():
            purchase = form.save(commit=False)
            # # Get selected payee ID from drop down box
            # payee = form.cleaned_data['payeeID']
            # Gets item purchased
            item_purchased = form.cleaned_data['itemID']
            # Get cost of transaction entered by user from form
            item_cost = form.cleaned_data['value']
            # Get this user's userprofile, where their balance is stored
            userprofile = UserProfile.objects.get_or_create(user=request.user)[0]
            # Gets item object to allow toggling of needsbought booleanfield - what is get or create?
            toggle_item_bought = Item.objects.get(id=item_purchased.id)

            # Reflect this on user's balance
            userprofile.balance += item_cost

            # Sets items needs bought status to false, for item model
            toggle_item_bought.itemNeedsBought = False

            # Updates the transaction model
            purchase.payeeID = request.user
            purchase.itemID = item_purchased

            # Saves changes
            userprofile.save()
            toggle_item_bought.save()
            purchase.save()
            form = RecordPurchase()

        else:
            print(form.errors)
    return form

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
        else:
             print(form.errors)
    return form

# View for sitemap
def sitemap(request):

    app_url = request.path

    # Get the user profile so profile sidebar can render balance.
    user_profile = getUserProfile(request)

    context_dict = {'app_url': app_url, 'userprofile':user_profile}

    response = render(request, 'MILK/sitemap.html', context_dict)
    return response

# View for contact us page
def contact(request):

    app_url = request.path

    # Get the user profile so profile sidebar can render balance.
    user_profile = getUserProfile(request)

    # Form to be displayed for users to contact the site.
    form = ContactForm()

    context_dict = {'app_url': app_url, 'form':form, 'userprofile':user_profile}

    return render(request, 'MILK/contact.html', context_dict)

def about(request):

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
            return redirect('profile', user.username)
        else:
            print(form.errors)

    return(form)

# View for a user's profile
@login_required
def profilepage(request, username):

    try:
        # May want to view another user's profile!
        user = User.objects.get(username=username)

        # User should only functionally have one group. If
        # it exists, we select it. If it doesn't, form won't
        # be rendered anyway.
        if user.groups.all().first() != None:
            group = user.groups.all().first()

    except User.DoesNotExist:
        return redirect('home')

    # Retrieve UserProfile extension (containing balance/picture).
    # We will then pass this to profile.html
    userprofile = UserProfile.objects.get_or_create(user=user)[0]

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
            return redirect('profile', user.username)
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
    add_form = AddUser()
    remove_form = RemoveUser(groupname)

    # If admin presses button to add user, do the following:
    if request.method == 'POST' and 'adduserbutton' in request.POST:
        add_form = AddUser(request.POST)

        # Deal with add_form
        if add_form.is_valid():
            selecteduser = add_form.cleaned_data['user_to_add']
            selecteduser.groups.add(groupname)
            print("User successfully added!")
        else:
            print(add_form.errors)

    # If admin presses button to remove user, instead do the following:
    if request.method == 'POST' and 'removeuserbutton' in request.POST:
        remove_form = RemoveUser(groupname, request.POST)

        # Deal with remove_form
        if remove_form.is_valid():
            selecteduserID = remove_form.cleaned_data['user_to_remove']
            # Filter user based on their ID
            selecteduser = User.objects.get(id=selecteduserID)
            selecteduser.groups.remove(groupname)
            print("User successfully removed!")
            return redirect('group', groupname)
        else:
            print(remove_form.errors)

    context_dict = {'currentgroup':groupname,
                    'groupdetail':groupdetail,
                    'user':user,
                    'addform':add_form,
                    'removeform':remove_form,
                    'members':groupmembers,
                    'userprofile':user_profile,}

    response = render(request, 'MILK/grouppage.html', context_dict)
    return response


def suggest_item(request):
    item_list = []
    starts_with = ''

    if request.method == 'GET':
        starts_with = request.GET['suggestion']
    item_list = get_item_list(8, starts_with)
    print "-------------------"
    print item_list

    return render(request, 'milk/items.html', {'Items': item_list})


def get_item_list(max_results=0, starts_with=''):
    item_list = []
    if starts_with:

        # Need to get the user group in here
        # so I can filter it to only show items not already in the group list

        # May also use a set to do this, to eliminate duplicates

        item_list = Item.objects.filter(itemName__istartswith=starts_with)

    if max_results > 0:
        if len(item_list) > max_results:
            item_list = item_list[:max_results]
    print item_list
    return item_list


def suggest_add_item(request):
    item_list = []
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']
        user = request.user
        usergroup = user.groups.all().first()

        print starts_with
    item_list = get_add_item_list(usergroup ,1, starts_with)
    print item_list

    return render(request, 'milk/add_items.html', {'Items': item_list})


def get_add_item_list(usergroup, max_results=0, starts_with=''):
    item_list = []
    if starts_with:
        # Need to get the user's group in here to filter by this and only show items
        # from their shopping list
        item_list = Item.objects.filter(itemName__istartswith=starts_with, itemNeedsBought = False, groupBuying = usergroup )

    if max_results > 0:
        if len(item_list) > max_results:
            item_list = item_list[:max_results]
    print item_list
    return item_list


def item_needs_bought(request):
    item_id = None
    if request.method == 'GET':
        item_id = request.GET['item_adding']
        print item_id
        print "----------------"
        item_to_add = Item.objects.get(itemName=item_id)
        if item_to_add:
            print item_to_add
            item_to_add.itemNeedsBought = True
            item_to_add.save()
    return HttpResponse(True)

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

def average_balances(request):

    current_group = request.GET['current_group']
    groupmembers = User.objects.filter(groups__name=current_group).order_by()
    total = 0
    nummembers = 0
    output = []
    # gets user name = v in groupmembers
    for v in groupmembers:
        user_profile = UserProfile.objects.get(user=v)
        money = user_profile.balance
        money = round(money, 2)
        total = total + money
        nummembers = nummembers + 1

    # Print statements to check above code
    average = total / nummembers
    average = round(average, 2)
    final_balance = 0
    for v in groupmembers:
        user_profile = UserProfile.objects.get(user=v)
        user = user_profile.user
        user_name = user.username
        user_balance = user_profile.balance
        user_float = float(user_balance)

        finalbalance = user_float - average

        if finalbalance < 0:
            finalbalance = abs(finalbalance)
            print "abs:"
            print finalbalance
            finalbalance = round(finalbalance, 2)
            finalbalstring = str(finalbalance)
            useroutput = user_name + " owes: " + finalbalstring
            output.append(useroutput)
        else:
            finalbalance = round(finalbalance, 2)
            finalbalstring = str(finalbalance)
            useroutput = user_name + " is owed: " + finalbalstring
            output.append(useroutput)
        final_balance = 0
    response = render(request, 'MILK/averaged_balances.html', {'user_balances': output})
    return (response)

# Helper method for making a json file
def jsonmaker(data):
    json_data = json.dumps(data)
    return json_data

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
