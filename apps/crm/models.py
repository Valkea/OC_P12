from django.db import models

# from django.conf import settings

from apps.users.models import EpicMember


class Client(models.Model):
    class Status(models.TextChoices):
        PROSPECT = "PROSPECT", "Potential Client"
        SIGNED = "SIGNED", "Current Client"
        OLD = "OLD", "Lost Client"

    sales_contact = models.ForeignKey(
        to=EpicMember,
        on_delete=models.SET_NULL,
        related_name="sales_contact_clients",
        null=True,
    )

    compagny_name = models.CharField("Company name", max_length=250)

    status = models.CharField(
        "Status", max_length=10, choices=Status.choices, default=Status.PROSPECT
    )
    contact_first_name = models.CharField("Contact first name", max_length=25)
    contact_last_name = models.CharField("Contact last name", max_length=25)
    contact_email = models.EmailField("Contact email", max_length=100)
    contact_mobile = models.CharField("Contact mobile", max_length=20)
    company_phone = models.CharField("Company phone", max_length=20)

    created_time = models.DateTimeField("Creation date", auto_now_add=True)
    updated_time = models.DateTimeField("Modification date", auto_now=True)


class Contract(models.Model):
    class Status(models.TextChoices):
        OPENED = "OPENED", "Waiting for a signature"
        SIGN = "SIGNED", "Signed"
        CLOSED = "PAID", "Paid"

    client = models.ForeignKey(
        to=Client,
        on_delete=models.CASCADE,
        related_name="client_contracts",
    )

    sales_contact = models.ForeignKey(
        to=EpicMember,
        on_delete=models.SET_NULL,
        related_name="sales_contact_contracts",
        null=True,
    )

    status = models.CharField(
        "Status", max_length=10, choices=Status.choices, default=Status.OPENED
    )
    amount = models.FloatField()

    payment_date = models.DateTimeField("Payment date")
    created_time = models.DateTimeField("Creation date", auto_now_add=True)
    updated_time = models.DateTimeField("Modification date", auto_now=True)


class Event(models.Model):
    class Status(models.TextChoices):
        OPENED = "OPENED", "Need a support contact"
        STEP_PLAN = "PLAN", "To planify"
        STEP_PREPARE = "PREPARE", "To prepare"
        STEP_PRODUCT = "PRODUCE", "To produce"
        STEP_PERFECT = "PERFECT", "To perfect"
        CLOSED = "CLOSED", "Closed"

    contract = models.ForeignKey(
        to=Contract,
        on_delete=models.CASCADE,
        related_name="contract_events",
    )

    support_contact = models.ForeignKey(
        to=EpicMember,
        on_delete=models.SET_NULL,
        related_name="support_contact_events",
        null=True,
    )

    status = models.CharField(
        "Status", max_length=10, choices=Status.choices, default=Status.OPENED
    )
    attendess = models.PositiveIntegerField()
    notes = models.TextField("Notes", max_length=8192)

    start_date = models.DateTimeField("Event starting date")
    close_date = models.DateTimeField("Event ending date")
    created_time = models.DateTimeField("Creation date", auto_now_add=True)
    updated_time = models.DateTimeField("Modification date", auto_now=True)
