from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
		

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()




def update_profile(sender, instance, created, **kwargs):
	if created == False:
		instance.profile.first_name = instance.first_name
		instance.profile.last_name = instance.last_name
		instance.profile.email = instance.email
		instance.profile.save()
		print("Profile updated!")

post_save.connect(create_profile, sender=User)
post_save.connect(update_profile, sender=User)


def update_username(sender, instance, **kwargs):
	instance.username = instance.email
	print("Username updated!", instance.username)

pre_save.connect(update_username, sender=User)