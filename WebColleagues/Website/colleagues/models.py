from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    photo = models.FileField(null=True)
    position = models.CharField(null=True, max_length=50)
    salary = models.FloatField(null=True)
    unused_vacation_days = models.PositiveIntegerField(null=True)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created: Profile.objects.create(user=instance)
    else: instance.profile.save()
