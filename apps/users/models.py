from django.db import models
from django.contrib.auth.models import AbstractUser


class EpicMember(AbstractUser):
    class Team(models.TextChoices):
        MANAGE = "MANAGE", "Managing team"
        SELL = "SELL", "Selling team"
        SUPPORT = "SUPPORT", "Support team"
        UNDEFINED = "NONE", "Need a team"

    first_name = models.CharField("First name", max_length=25)
    last_name = models.CharField("Last name", max_length=25)
    email = models.EmailField("Email", max_length=100)

    team = models.CharField(
        "Status", max_length=10, choices=Team.choices, default=Team.UNDEFINED
    )

    created_time = models.DateTimeField("Creation date", auto_now_add=True)
    updated_time = models.DateTimeField("Modification date", auto_now=True)
