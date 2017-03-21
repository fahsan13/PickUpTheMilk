from django.test import TestCase
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
        trans.save()
        self.assertEqual((trans.value>0), True)










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

def add_group(name,):
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
