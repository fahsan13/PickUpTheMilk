#"Populating Pick Up The Milk, this population script provides three scenarios."
#"1. The Group LanceSamanthaandPaulsFlat: Lance Samantha and Paul are having a party, they each add one item they wish to have for the party to the list, and each purchase one item"
#"2. The Group 2WillowbankSt: Edwin, Julie and Lisa have a group for their shared flat, they have items that they need to purchase, but no one has gone to the shops yet"
#"3. The users BillFlower and BenPotMan: these are two individual users who do not currently have a group, could be used to test creating a group and adding new members"
#"NOTE: all users created here have password test12345 should you wish to log in as them "




import os
#file_path = os.path.join(BASE_DIR, 'relative_path')
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pickUpTheMilk.settings')
from django.core.files import File
django.setup()

from MILK.models import Group, GroupDetail, User, UserProfile, Item, Transaction

def populate():



    partygroup = [
         "LanceSamanthaandPaulsFlat",
    ]
    partyuser = [
        {"username" : "LanceSteel", "email" : "lanceismgtow@liftweights.com", "balance" : 4.00, "picture" : File(open("media/profile_images/ghost.jpg"))},
        {"username" : "SamanthaCowlove", "email" : "sheeparefriends@notfood.com", "balance" : 7.00, "picture" : File(open("media/profile_images/broccoli.jpg"))},
        {"username" : "PaulOtherGuy", "email" : "paul@hasnopersona.com", "balance" : 8.00, "picture" : File(open("media/profile_images/milk.jpg"))}
        ]
    partyitem = [
        {"itemName" : "plastic cups", "groupBuying": "LanceSamanthaandPaulsFlat", "addedby" : "LanceSteel"},
        {"itemName" : "ice", "groupBuying":"LanceSamanthaandPaulsFlat", "addedby" : "SamanthaCowlove"},
        {"itemName" : "party poppers", "groupBuying": "LanceSamanthaandPaulsFlat", "addedby" : "PaulOtherGuy"}
    ]
    partytransaction =  [
        {"payeeID" : "LanceSteel", "itemID" : "ice", "value" : 4.00 },
        {"payeeID" : "SamanthaCowlove", "itemID" : "party poppers", "value" : 7.00 },
        {"payeeID" : "PaulOtherGuy", "itemID" : "plastic cups", "value" : 8.00}
    ]
    for a in partygroup:
        group_created = add_group(a)
    for b in partyuser:
        if b["username"] == "LanceSteel":
            the_admin = add_user(b["username"], b["email"], b["balance"], b["picture"], group_created)
            set_admin(group_created, the_admin)
        else:
            add_user(b["username"], b["email"], b["balance"], b["picture"], group_created)
    for c in partyitem:
        for z in partyuser:
            if z["username"] == c["addedby"]:
                added_by = User.objects.get(username = z["username"])
                add_item(c["itemName"], group_created, added_by)
    for d in partytransaction:
        for y in partyuser:
            if y["username"] == d["payeeID"]:
                payee = User.objects.get(username = y["username"])
                for x in partyitem:
                    if x["itemName"]== d["itemID"]:
                        the_item = Item.objects.get(itemName = d["itemID"])
                        add_transaction(the_item, payee, d["value"])


    sandwichgroup = [
         "2WillowbankSt",
    ]
    sandwichuser = [
        {"username" : "Edwin", "email" : "edwin@magic.com", "balance" : 0.00, "picture" : File(open("media/profile_images/ghost.jpg"))},
        {"username" : "Julie", "email" : "julie@secret.com", "balance" : 0.00, "picture" : File(open("media/profile_images/broccoli.jpg"))},
        {"username" : "Lisa", "email" : "lisa@keys.com", "balance" : 0.00, "picture" : File(open("media/profile_images/milk.jpg"))},
        ]
    sandwichitem = [
        {"itemName" : "bread", "groupBuying": "2WillowbankSt", "addedby" : "Edwin"},
        {"itemName" : "cheese", "groupBuying":"2WillowbankSt", "addedby" : "Julie"},
        {"itemName" : "ham", "groupBuying": "2WillowbankSt", "addedby" : "Lisa"}
    ]
    for a in sandwichgroup:
        group_created = add_group(a)
    for b in sandwichuser:
        if b["username"] == "Lisa":
            the_admin = add_user(b["username"], b["email"], b["balance"], b["picture"], group_created)
            set_admin(group_created, the_admin)
        else:
            add_user(b["username"], b["email"], b["balance"], b["picture"], group_created)
    for c in sandwichitem:
        for z in sandwichuser:
            if z["username"] == c["addedby"]:
                added_by = User.objects.get(username = z["username"])
                add_item(c["itemName"], group_created, added_by)

    lonelyuser = [
        {"username" : "BillFlower", "email" : "bill@thegarden.com", "balance" : 0.00,"picture" : File(open("media/profile_images/ghost.jpg"))},
        {"username" : "BenPotMan", "email" : "ben@thegarden.com", "balance" : 0.00,"picture" : File(open("media/profile_images/broccoli.jpg"))},
        {"username" : "ParsleyTheLion", "email" : "parsley@thelion.com", "balance" : 0.00, "picture" : File(open("media/profile_images/milk.jpg"))},
        ]


    for a in lonelyuser:
        add_user_no_group(a["username"], a["email"], a["balance"], a["picture"])




def add_user(username, email, balance, pic, group):
    u = User.objects.get_or_create(username = username, email = email)[0]
    u.save()
    u.groups.add(group)
    u.set_password("test12345")
    u.save()
    up = UserProfile.objects.get_or_create(user = u, balance = balance, picture = pic)
    return u

def add_user_no_group(username, email, balance, pic):
    u = User.objects.get_or_create(username = username, email = email)[0]
    u.save()
    u.set_password("test12345")
    u.save()
    up = UserProfile.objects.get_or_create(user = u, balance = balance, picture = pic)
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

def add_transaction(itemID, payeeID, value):
    t = Transaction.objects.get_or_create(itemID = itemID, payeeID = payeeID, value = value)[0]
    t.save()
    return t


if __name__ == '__main__':
    print "Populating Pick Up The Milk, this population script provides three scenarios."
    print "1. The Group LanceSamanthaandPaulsFlat: Lance Samantha and Paul are having a party, they each add one item they wish to have for the party to the list, and each purchase one item"
    print "2. The Group 2WillowbankSt: Edwin, Julie and Lisa have a group for their shared flat, they have items that they need to purchase, but no one has gone to the shops yet"
    print "3. The users BillFlower and BenPotMan: these are two individual users who do not currently have a group, could be used to test creating a group and adding new members"
    print "NOTE: all users created here have password test12345 should you wish to log in as them "
    populate()
