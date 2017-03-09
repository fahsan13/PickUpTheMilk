# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-03-09 10:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(max_length=128, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itemName', models.CharField(max_length=128, unique=True)),
                ('itemNeedsBought', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ItemToUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itemID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MILK.Item')),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listID', models.IntegerField(default=0, unique=True)),
                ('listName', models.CharField(max_length=128)),
                ('itemQuantity', models.IntegerField(default=1)),
                ('itemID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MILK.Item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ID', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requestID', models.IntegerField(default=0, unique=True)),
                ('value', models.DecimalField(decimal_places=2, max_digits=6)),
                ('itemQuantity', models.IntegerField(default=1)),
                ('DateandTime', models.DateTimeField(auto_now_add=True)),
                ('itemID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactionItem', to='MILK.Item')),
                ('payeeID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payeeID', to=settings.AUTH_USER_MODEL)),
                ('purchaserID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchaserID', to=settings.AUTH_USER_MODEL)),
                ('requestorID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requestorID', to='MILK.ItemToUser')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('picture', models.ImageField(blank=True, upload_to=b'profile_images')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserToGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groupID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MILK.Group')),
                ('userID', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserToList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MILK.ShoppingList')),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='administrator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MILK.UserProfile'),
        ),
    ]
