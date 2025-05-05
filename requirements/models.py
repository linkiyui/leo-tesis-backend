from django.db import models
from user.models import User
import uuid
# Create your models here.
class RequirementProvider(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    adscription = models.CharField(max_length=255, null=False, blank=False)
    charge = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(max_length=255, null=False, blank=False)
    phone_number = models.CharField(max_length=255, null=False, blank=False)
    address = models.CharField(max_length=255, null=False, blank=False)
    business_knowledge = models.IntegerField( null=False, blank=False)
    market_knowledge = models.IntegerField( null=False, blank=False) 
    time_availability = models.IntegerField( null=False, blank=False) 
    comunication_skills = models.IntegerField( null=False, blank=False)
    system_interaction = models.IntegerField( null=False, blank=False)
    autority_range = models.IntegerField( null=False, blank=False)
    informatic_knowledge = models.IntegerField( null=False, blank=False)
    project_compromise = models.IntegerField( null=False, blank=False)
    puntuation = models.FloatField( null=False, blank=False)
    result = models.CharField(max_length=255, null=False, blank=False)
    ranking = models.IntegerField( null=False, blank=False)
    auxiliary = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    aproved_at = models.DateTimeField(null=True, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.id
    

    def get_puntuation(self):
        matriz = [0.16, 0.16, 0.13, 0.10, 0.10, 0.16, 0.06, 0.13 ]

        puntuation = (self.business_knowledge * matriz[0] + self.market_knowledge * matriz[1] + self.time_availability * matriz[2] + self.comunication_skills * matriz[3] + self.system_interaction * matriz[4] + self.autority_range * matriz[5] + self.informatic_knowledge * matriz[6] + self.project_compromise * matriz[7])


        return puntuation
    
    def get_result(self):
        if self.puntuation >= 3:
            return "apto"
        else:
            return "no apto"

class ClientNeeds(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.IntegerField(null=False, blank=False)
    needed = models.CharField(max_length=255, null=False, blank=False)
    important = models.IntegerField(null = False , blank=False)
    urgency = models.IntegerField(null = False, blank=False)
    created_at = models.DateTimeField(null=False , blank=False)
    requirement_provider_id = models.ForeignKey(RequirementProvider , on_delete=models.CASCADE)

    def __str__(self):
        return self.needed
    

class RequirementClient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.IntegerField(null=False, blank=False)
    solicited_requirement = models.CharField(max_length=255, null=False, blank=False)
    solicited_at = models.DateTimeField(null=False, blank=False)
    is_modified = models.BooleanField(null=False, blank=False)
    is_tracked = models.BooleanField(null=False, blank=False)
    decision = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(null=False, blank=False)
    requirement_provider_id = models.ForeignKey(RequirementProvider, on_delete=models.CASCADE)
    client_needs_id = models.ForeignKey(ClientNeeds, on_delete=models.CASCADE)

    def __str__(self):
        return self.solicited_requirement