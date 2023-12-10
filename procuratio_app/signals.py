from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *
from django.contrib.auth.models import Group

@receiver(post_save, sender=Utilisateur)
def create_admin(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser == True:
            admin_group_name = 'AdminGroup'
            user_group, created = Group.objects.get_or_create(name=admin_group_name)
        else:
            client_group_name = 'ClientGroup'
            user_group, created = Group.objects.get_or_create(name=client_group_name)
        instance.groups.add(user_group)


post_save.connect(create_admin, sender=Utilisateur)
