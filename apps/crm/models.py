from django.db import models

# from django.conf import settings

from apps.users.models import EpicMember


class Status(models.Model):
    class Meta:
        unique_together = (("table", "value"),)
        verbose_name = "Status"
        verbose_name_plural = "Status"

    class Table(models.TextChoices):
        CLIENT = "CLIENT", "Client status"
        CONTRACT = "CONTRACT", "Contract status"
        EVENT = "EVENT", "Event status"

    table = models.CharField(
        "Table",
        max_length=10,
        choices=Table.choices,
        default=Table.CLIENT,
    )

    value = models.CharField("Database value", max_length=20)
    label = models.CharField("Displayed value", max_length=100)

    def __str__(self):
        return f"{self.label}"


class Client(models.Model):

    sales_contact = models.ForeignKey(
        to=EpicMember,
        on_delete=models.SET_NULL,
        related_name="sales_contact_clients",
        null=True,
        blank=True,
        limit_choices_to={"team": EpicMember.Team.SELL},
    )

    company_name = models.CharField("Company name", max_length=250)

    status = models.ForeignKey(
        to=Status,
        on_delete=models.PROTECT,
        limit_choices_to={"table": Status.Table.CLIENT},
        null=True,
        blank=True,
    )

    contact_first_name = models.CharField(
        "Contact first name", max_length=25, null=True, blank=True
    )
    contact_last_name = models.CharField(
        "Contact last name", max_length=25, null=True, blank=True
    )
    contact_email = models.EmailField(
        "Contact email", max_length=100, null=True, blank=True
    )
    contact_mobile = models.CharField(
        "Contact mobile", max_length=20, null=True, blank=True
    )
    company_phone = models.CharField(
        "Company phone", max_length=20, null=True, blank=True
    )

    created_time = models.DateTimeField("Creation date", auto_now_add=True)
    updated_time = models.DateTimeField("Modification date", auto_now=True)

    def __str__(self):
        contact = " ".join(
            [x for x in [self.contact_first_name, self.contact_last_name] if x]
        )
        if contact != "":
            contact = f" [{contact}]"
        return f"{self.company_name}{contact}"


class Contract(models.Model):

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
        blank=True,
        limit_choices_to={"team": EpicMember.Team.SELL},
    )

    status = models.ForeignKey(
        to=Status,
        on_delete=models.PROTECT,
        limit_choices_to={"table": Status.Table.CONTRACT},
        null=True,
        blank=True,
    )

    amount = models.FloatField(null=True, blank=True)

    payment_date = models.DateField("Payment date", null=True, blank=True)
    created_time = models.DateTimeField("Creation date", auto_now_add=True)
    updated_time = models.DateTimeField("Modification date", auto_now=True)

    def __str__(self):
        return f"Contract N°{self.id}"


class Event(models.Model):

    name = models.CharField("Event name", max_length=250)

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
        blank=True,
        limit_choices_to={"team": EpicMember.Team.SUPPORT},
    )

    status = models.ForeignKey(
        to=Status,
        on_delete=models.PROTECT,
        related_name="status_events",
        limit_choices_to={"table": Status.Table.EVENT},
        null=True,
        blank=True,
    )

    attendees = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField("Notes", max_length=8192, null=True, blank=True)

    start_date = models.DateTimeField("Event starting date", null=True, blank=True)
    close_date = models.DateTimeField("Event ending date", null=True, blank=True)
    created_time = models.DateTimeField("Creation date", auto_now_add=True)
    updated_time = models.DateTimeField("Modification date", auto_now=True)

    def __str__(self):
        return self.name
