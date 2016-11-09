from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.db.models.signals import post_save


@python_2_unicode_compatible
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    location = models.CharField(max_length=140, blank=True, null=True)
    gender = models.CharField(
        max_length=140, choices=GENDER_CHOICES, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    company = models.CharField(max_length=50, blank=True, null=True)
    website = models.URLField(max_length=50, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='user_avatars', blank=True, null=True)

    def __str__(self):
        return self.user.username


def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

# Signal while saving user
post_save.connect(create_profile, sender=User)
