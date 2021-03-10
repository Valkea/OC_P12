from django.db import models
from django.contrib.auth.models import AbstractUser  # , BaseUserManager


class EpicMember(AbstractUser):
    class Team(models.TextChoices):
        MANAGE = "MANAGE", "Managing team"
        SELL = "SELL", "Sales team"
        SUPPORT = "SUPPORT", "Support team"
        UNDEFINED = "NONE", "Need a team"

    first_name = models.CharField("First name", max_length=25, null=True, blank=True)
    last_name = models.CharField("Last name", max_length=25, null=True, blank=True)
    email = models.EmailField("Email", max_length=100, null=True, blank=True)
    password = models.CharField("Password", max_length=100, null=False, blank=False)

    team = models.CharField(
        "Team", max_length=10, choices=Team.choices, default=Team.UNDEFINED
    )

    created_time = models.DateTimeField("Creation date", auto_now_add=True)
    updated_time = models.DateTimeField("Modification date", auto_now=True)
