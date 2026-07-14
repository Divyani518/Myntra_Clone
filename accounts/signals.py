from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile, create_profile

post_save.connect(create_profile, sender=User)
