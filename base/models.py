from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True, unique=True)  # unique=True so no other user can log in with the same email
    bio = models.TextField(null=True, blank=True)
    event_participant = models.BooleanField(default=True, null=True)
    avatar= models.ImageField(default= 'avatar.png')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)



    # Modifications to the login Sequence
    USERNAME_FIELD = 'email'   #this make the email field the default login 
    REQUIRED_FIELDS = ['username'] #this make the required fields the default

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participant = models.ManyToManyField(User, blank=True, related_name='events') # the related_name shows all the event associted with the user
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    registration_deadline = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    

    def __str__(self):
        return self.name


class Submission(models.Model):
    participant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='submissions')  # THis leaves a record of the submission that was deleted
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True) 
    details = models.TextField(null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)



    def __str__(self):
        return str(self.event) + '------' + str(self.participant)  # This shows the event and the user that posted this