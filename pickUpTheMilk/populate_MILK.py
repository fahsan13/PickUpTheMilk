import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pickUpTheMilk.settings')
django.setup()

from MILK.models import Group, GroupDetail, User, UserProfile, Item, Transaction

def populate():

    group = [
         "Lance, Samantha and Paul's Flat"
    ]

    user = [
        {"username" : "LanceSteel", "email" : "lanceismgtow@liftweights.com", "balance" : 4.00,},
        {"username" : "SamanthaCowlove", "email" : "sheeparefriends@notfood.com", "balance" : 7.00,},
        {"username" : "PaulOtherGuy", "email" : "paul@hasnopersona.com", "balance" : 8.00,}
        ]

    # Lance Samantha and Paul are having a party
    item = [
        {"itemName" : "plastic cups", "groupBuying": "Lance, Samantha and Paul's Flat", "addedby" : "LanceSteel"},
        {"itemName" : "ice", "groupBuying": "Lance, Samantha and Paul's Flat", "addedby" : "SamanthaCowlove"},
        {"itemName" : "party poppers", "groupBuying": "Lance, Samantha and Paul's Flat", "addedby" : "PaulOtherGuy"}
    ]

    transaction =  [
        {"payeeID" : "LanceSteel", "itemID" : "ice", "value" : 4.00 },
        {"payeeID" : "SamanthaCowlove", "itemID" : "party poppers", "value" : 7.00 },
        {"payeeID" : "PaulOtherGuy", "itemID" : "plastic cups", "value" : 8.00}
    ]

    for a in group:
        group_created = add_group(a)

    for b in user:
        if b["username"] == "LanceSteel":
            the_admin = add_user(b["username"], b["email"], b["balance"], group_created,)
            set_admin(group_created, the_admin)
        else:
            add_user(b["username"], b["email"], b["balance"], group_created,)



        #for y in group_detail:
        #    add_group_detail(group_created, the_admin)

    for x in item:
        add_item(x["itemName"], group_added, x["addedby"])
    for x in transaction:
        add_transaction(x)


def add_user(username, email, balance, group):
    u = User.objects.get_or_create(username = username, email = email)[0]

    u.save()
    u.groups.add(group)
    u.set_password("test12345")
    u.save()
    up = UserProfile.objects.get_or_create(user = u, balance = balance)
    return u

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

def add_transaction(payeeID, itemID, value):
    t = Transaction.object.get_or_create(itemName = itemName)[0]
    t.payeeID = payeeID
    t.itemID = itemID
    t.value = value
    t.save()
    return t


if __name__ == '__main__':
    print "Populating Pick Up The Milk"
    populate()
