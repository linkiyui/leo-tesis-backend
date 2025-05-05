from django.db import models
import uuid

# Create your models here.
class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100 , unique=True , null=False , blank=False)
    email = models.EmailField(max_length=100 , unique=True , null=False , blank=False)
    password = models.CharField(max_length=100 , null=False , blank=False)

    def __str__(self):
        return self.username


