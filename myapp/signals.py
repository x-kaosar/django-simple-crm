from django.contrib.auth.models import User,Group
from django.db.models.signals import post_save
from .models import Customer
from django.dispatch import receiver


def customer_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)
        Customer.objects.create(
            user=instance,
            name=instance.username,
            email=instance.email
        )
        print('Profile created!')

post_save.connect(customer_profile, sender=User)


def update_customer(sender, instance, created, **kwargs):
    if created == False:
        instance.customer.save()

        print('Profile Updated!')

post_save.connect(update_customer, sender=User)