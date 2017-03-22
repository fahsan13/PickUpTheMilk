from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from  MILK.models import User, Group, Item, GroupDetail, UserProfile, Transaction


class UserProfileMethodTests(TestCase):
    def test_ensure_balances_are_positive(self):
        """
        ensure_balances_are_positive should result True for categories
        where views are zero or positive
        """
        u = add_user_no_group(username = "test", email = "test@test.com", balance = -1)
        self.assertEqual((u.balance >= 0), True)


    def test_ensure_transactions_are_positive(self):
        """
        ensure_transactions_are_positive should retult True for categories
        where value is positive and greater than zero
        """
        #prerequisite setup
        group = add_group("testgroup")
        user = add_user("testuser", "test@test.com", 0, group)

        item = add_item("testitem", group, user)
        item.save()


        trans = add_transaction(item, user, 0)
        self.assertEqual((trans.value>0), True)


    def test_ensure_home_shows_all_groups_items_when_loggedin(self):
        """"
        Check to ensure that a user's items are displayed on their home page
        """
        #create a dummy group and user
        group = add_group("testgroup")
        user = add_user("testuser", "test@test.com", 0, group)
        #login the user
        self.client.login(username='testuser', password='test12345')

        #create four related items
        add_item("testbread", group, user)
        add_item("testmilk", group, user)
        add_item("testlooroll", group, user)
        add_item("testbread testmilk testlooroll", group, user)

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testbread testmilk testlooroll")
        num_items =len(response.context['Items'])
        self.assertEqual(num_items, 4)


    def test_ensure_users_balance_displays_correctly(self):
        """"
        Check a user's balance displays correctly on their profile page
        """
        #create a dummy group and user
        group = add_group("testgroup")
        u = add_user("testuser", "test@test.com", 9.00, group)
        #login the user
        self.client.login(username='testuser', password='test12345')
        response = self.client.get(reverse('profile', args =['testuser']))
        self.assertEqual(response.status_code, 200)
        c =Client()
        u = response.context['userprofile']
        the_balance = u.balance
        self.assertEqual(the_balance, 9.00)


    def test_group_page_shows_all_members(self):
        """
        Check that a user without groups profile displays properly
        """
        #create a dummy group and several users
        group = add_group("testgroup")
        u1 = add_user("testuser1", "test1@test.com", 0.00, group)
        u2 = add_user("testuser2", "test2@test.com", 0.00, group)
        u3 = add_user("testuser3", "test3@test.com", 0.00, group)
        #login a user
        self.client.login(username='testuser1', password='test12345')

        response = self.client.get(reverse('group', args =['testgroup']))
        self.assertContains(response, "testuser3")
        num_members =len(response.context['members'])
        self.assertEqual(num_members, 3)

    def test_userprofile_without_group(self):

        add_user_no_group("testuser1", "test1@test.com", 0.00)
        #login a user
        self.client.login(username='testuser1', password='test12345')
        response = self.client.get(reverse('profile', args =['testuser1']))
        self.assertContains(response, "Not a member of any groups")
























######### HELPER METHODS #########
def add_user(username, email, balance, group):
    u = User.objects.get_or_create(username = username, email = email)[0]
    u.save()
    u.groups.add(group)
    u.set_password("test12345")
    u.save()
    up = UserProfile.objects.get_or_create(user = u, balance = balance)
    return u

def add_user_no_group(username, email, balance):
    u = User.objects.get_or_create(username = username, email = email)[0]
    u.save()
    u.set_password("test12345")
    u.save()
    up = UserProfile.objects.create(user = u, balance = balance)
    up.save()
    return up

def add_group(name):
    g = Group.objects.get_or_create(name = name)[0]
    g.save()
    gd = GroupDetail.objects.get_or_create(group = g)[0]
    gd.save()
    return g


def set_admin(group, the_admin):
    g = GroupDetail.objects.get(group = group)
    g.administrator = the_admin
    g.save()


def add_item(itemName, groupBuying, addedby):
    i = Item.objects.get_or_create(itemName = itemName)[0]
    i.groupBuying = groupBuying
    i.addedby = addedby
    i.save()
    return i

def add_transaction(itemID, payeeID, value):
    t = Transaction.objects.get_or_create(itemID = itemID, payeeID = payeeID, value = value)[0]
    t.save()
    return t
