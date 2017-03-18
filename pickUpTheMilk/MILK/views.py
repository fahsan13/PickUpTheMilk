from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Sum

from MILK.models import User, UserProfile, Group, GroupDetail, Item
from MILK.forms import itemForm, groupForm, UserProfileForm, AddUser, RemoveUser, RecordPurchase, needsBoughtForm, ContactForm
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
    # Placed here assuming we're keeping lists on home page? if I'm wrong, easy to change
    item_list = Item.objects.order_by('id')
    app_url = request.path

    context_dict = {'Items': item_list, 'app_url': app_url }
    response = render(request, 'MILK/home.html', context_dict)
    return response

def sitemap(request):
    app_url = request.path
    response = render(request, 'MILK/sitemap.html', {'app_url': app_url})
    return response

def contact(request):

    app_url = request.path

    form = ContactForm()

    return render(request, 'MILK/contact.html', {'app_url': app_url, 'form':form})

def about(request):
    app_url = request.path
    return render(request, 'MILK/about.html', {'app_url': app_url})

def parralax(request):
    app_url = request.path
    return render(request, 'MILK/parralax.html', {'app_url': app_url})



# View for create-group.html.
# Need to implement error handling for when
# group with a given name already exists IF
# we don't later refactor this so that we use
# group IDs in URLs instead of unique group names but thats
# a bit harder and I can't be bothered right now.
@login_required
def creategroup(request):

    form = groupForm(request.POST)

    # Get currently logged in user.
    user=request.user
    # get their user profile
    user_profile = UserProfile.objects.get(user = user)

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

    response = render(request, 'MILK/create-group.html', {'form':form, 'userprofile': user_profile})
    return response

# View for a user's profile
def profilepage(request, username):

    try:
        # May want to view another user's profile!
        user = User.objects.get(username=username)
        # User should only functionally have one group. If
        # it exists, we select it. If it doesn't, form won't
        # be rendered anyway.
        if user.groups.all().first() != None:
            group = user.groups.all()[0]

    except User.DoesNotExist:
        return redirect('home')

    # Retrieve UserProfile extension (containing balance/picture).
    # We will then pass this to profile.html
    userprofile = UserProfile.objects.get_or_create(user=user)[0]

    if request.method == 'POST':
        form = itemForm(request.POST)
        if form.is_valid():
            item=form.save(commit=False)
            # Assign the user who added the item and the group it belongs to
            item.addedby = user
            item.groupBuying = group
            item.save()
        else:
            print(form.errors)
    else:
        # Not a post, so just render empty form
        form = itemForm()

    # Get items so we can display on user's page
    item_list = Item.objects.order_by('id')
    context_dict = {'Items': item_list, 'form':form, 'selecteduser':user, 'userprofile': userprofile,}
    app_url = request.path
    response = render(request, 'MILK/userprofile.html', {'form':form, 'selecteduser':user, 'userprofile': userprofile})

    response = render(request, 'MILK/userprofile.html', context_dict)
    return response

# View for communal group page
@login_required
def grouppage(request, groupname):

    # Get current user
    user=request.user
    # Get all members of the group
    groupmembers = User.objects.filter(groups__name=groupname)

    try:
        # No idea why this is working; change groupname
        # reference on left and it breaks :/
        groupname = Group.objects.get(name=groupname)
        groupdetail = GroupDetail.objects.get(group=groupname)
    except Group.DoesNotExist:
        return redirect('home')

    # Not a POST, so just render empty form
    add_form = AddUser()
    remove_form= RemoveUser(groupname)

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
        else:
            print(remove_form.errors)

    response = render(request, 'MILK/grouppage.html',  {'currentgroup':groupname, 'groupdetail':groupdetail, 'user':user, 'addform':add_form, 'removeform':remove_form, 'members':groupmembers})
    return response

@login_required
#Should be record purchase. Since we are recording a purchase.
def record_purchase(request):

    form=RecordPurchase()

    if request.method == 'POST':
        form = RecordPurchase(request.POST)

        if form.is_valid():
            purchase=form.save(commit=False)
            # Get selected payee ID from drop down box
            payee=form.cleaned_data['payeeID']
            # Gets item purchased
            item_purchased = form.cleaned_data['itemID']
            # Get cost of transaction entered by user from form
            item_cost = form.cleaned_data['value']
            # Get this user's userprofile, where their balance is stored
            userprofile = UserProfile.objects.get_or_create(user=payee)[0]
            # Gets item object to allow toggling of needsbought booleanfield - what is get or create?
            toggle_item_bought = Item.objects.get(id=item_purchased.id)

            # Reflect this on user's balance
            userprofile.balance += item_cost

            # Sets items needs bought status to false, for item model
            toggle_item_bought.itemNeedsBought = False

            # Updates the transaction model
            purchase.payeeID = payee
            purchase.itemID = item_purchased

            # Saves changes
            userprofile.save()
            toggle_item_bought.save()
            purchase.save()

        else:
             print(form.errors)

    response = render(request, 'MILK/transaction.html', {'form':form})
    return response

@login_required
#Temporary page for modelling item needing bought logic
def needsbought(request):

    #Imports form used to display items which aren't currently marked as needing to be bought
    form= needsBoughtForm()

    if request.method == 'POST':
        form = needsBoughtForm(request.POST)

        if form.is_valid():
            #needsBought=form.save(commit=False)

            # Gets item to set as needing bought
            item_needing_bought = form.cleaned_data['itemID']

            # Sets items needs bought status to false, for item model
            item_needing_bought.itemNeedsBought = True

            # Saves change
            item_needing_bought.save()

        else:
             print(form.errors)

    response = render(request, 'MILK/needsBought.html', {'form':form})
    return response


def get_item_list(max_results=0, starts_with=''):
    item_list = []
    if starts_with:
        item_list = Item.objects.filter(itemName__istartswith=starts_with)

    if max_results > 0:
        if len(item_list) > max_results:
            item_list = item_list[:max_results]
    print item_list
    return item_list

def suggest_item(request):
    item_list = []
    starts_with = ''

    if request.method == 'GET':
        starts_with = request.GET['suggestion']
    item_list = get_item_list(8, starts_with)

    '''Not 100% on how to pass items through to base to display
    in auto-complete form. Made Items.html as a placeholder
    to follow Tango with Django book. Not a robust solution, though'''
    return render(request, 'milk/Items.html', {'Items': item_list})


#Settle up page, resolve balances
@login_required
def settleup(request,groupname):
    # Get all members of the group
    groupmembers = User.objects.filter(groups__name=groupname)

    response = render(request, 'MILK/settle-up.html',{'members':groupmembers,})
    return response

#From early attempt to integrate AJAX for resolving balances, may scrap it
@login_required
def resolveBalances(request, groupname):
    current_group = User.objects.filter(groups__name=groupname)
    print "Do I get reached?"
    for each in current_group.objects.all():
        print "Am I looping?"
        userTo0 = current_group.object.username
        clearUserBalance(userTo0)
    return HttpResponse(something)


# Helper method to clear balance of an individual user
#From early attempt to integrate AJAX for resolving balances, may scrap it
def clearUserBalance(username):
    userprofile = UserProfile.objects.get_or_create(user=username)[0]
    userprofile.balance = 0
    userprofile.save()
    return response

