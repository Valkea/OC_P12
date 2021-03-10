import datetime

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from apps.users.models import EpicMember
from apps.crm.models import Client, Contract, Event


def printname(function):
    def wrapper(*args, **kwargs):
        print(f"\n[{function.__name__}]", end="")
        return function(*args, **kwargs)

    return wrapper


class EventsTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_url = reverse("token_obtain_pair")

        cls.profiles = {
            "manage1": {
                "username": "eve_demo_user_ma1",
                "email": "eve_userma1@foo.com",
                "password": "demopass1",
                "team": EpicMember.Team.MANAGE,
            },
            "sales1": {
                "username": "eve_demo_user_sa1",
                "email": "eve_usersa1@foo.com",
                "password": "demopass1",
                "team": EpicMember.Team.SELL,
            },
            "sales2": {
                "username": "eve_demo_user_sa2",
                "email": "eve_usersa2@foo.com",
                "password": "demopass2",
                "team": EpicMember.Team.SELL,
            },
            "support1": {
                "username": "eve_demo_user_su1",
                "email": "eve_usersu1@foo.com",
                "password": "demopass1",
                "team": EpicMember.Team.SUPPORT,
            },
            "support2": {
                "username": "eve_demo_user_su2",
                "email": "eve_usersu2@foo.com",
                "password": "demopass2",
                "team": EpicMember.Team.SUPPORT,
            },
            "noteam": {
                "username": "eve_demo_user_no1",
                "email": "eve_userno1@foo.com",
                "password": "demopass1",
                "team": "NONE",
            },
            "NOT_IN_DB": {
                "username": "",
                "email": "",
                "password": "",
                "team": "",
            },
        }

        for k, profile in cls.profiles.items():
            if k != "NOT_IN_DB":
                u = EpicMember.objects.create_user(
                    username=profile["username"],
                    email=profile["email"],
                    password=profile["password"],
                    team=profile["team"],
                )
                u.save()
                profile["instance"] = u

        # CLIENT

        cls.client01 = Client.objects.create(
            company_name="Contract test 01",
            sales_contact=cls.profiles["sales1"]["instance"],
        )

        cls.client01.save()
        cls.client01_url = reverse("client", args=[cls.client01.id])

        # CONTRACTS
        cls.contract01 = Contract.objects.create(
            client=cls.client01,
            sales_contact=cls.profiles["sales1"]["instance"],
        )
        cls.contract01.save()

        cls.contract02 = Contract.objects.create(
            client=cls.client01,
            sales_contact=cls.profiles["sales2"]["instance"],
        )
        cls.contract02.save()

        cls.contract03 = Contract.objects.create(
            client=cls.client01,
            sales_contact=cls.profiles["sales1"]["instance"],
        )
        cls.contract03.save()

        cls.event_list_url = reverse(
            "client_contract_events", args=[cls.client01.id, cls.contract01.id]
        )

        cls.event999_url = reverse(
            "client_contract_event", args=[cls.client01.id, cls.contract01.id, 999]
        )

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # --- HELPERS FUNCTIONS ---

    def login(self, profile):
        resp = self.client.post(
            self.login_url,
            {
                "username": self.profiles[profile]["username"],
                "password": self.profiles[profile]["password"],
            },
            format="json",
        )
        self.token = resp.data["access"]
        self.contract = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + self.token)

    def helper_create_event(self, old_contract=None):

        if old_contract is None:
            old_contract = self.contract01

        event = Event.objects.create(
            contract=old_contract,
            support_contact=self.profiles["support1"]["instance"],
        )

        event.save()
        event_url = reverse(
            "client_contract_event",
            args=[self.client01.id, old_contract.id, event.id],
        )

        return event, event_url

    # CREATES

    def helper_event_new(self, profile, new_contract="", support_contact=""):
        self.login(profile)

        if support_contact == "NOT_IN_DB":
            support_contact = 999
        elif support_contact != "":
            support_contact = self.profiles[support_contact]["instance"].id

        if new_contract == "NOT_IN_DB":
            new_contract = 999
        elif new_contract != "":
            new_contract = new_contract.id

        resp = self.client.post(
            self.event_list_url,
            {
                "name": "Demo Event Name",
                "contract": new_contract,
                "support_contact": support_contact,
            },
            format="json",
        )

        return resp

    def helper_event_new_full(self, set_wrong_format=False):

        if set_wrong_format:
            incomingDate = self.get_incoming_datetime_WRONG_FORMAT()
        else:
            incomingDate = self.get_incoming_datetime_RIGHT_FORMAT()

        resp = self.client.post(
            self.event_list_url,
            {
                "name": "Demo Event Name",
                "contract": self.contract01.id,
                "support_contact": self.profiles["support1"]["instance"].id,
                "status": "OPENED",
                "attendees": 1500,
                "notes": "Bla bla",
                "start_date": incomingDate,
                "close_date": incomingDate,
            },
            format="json",
        )

        return resp

    def helper_event_new_min(self):
        resp = self.client.post(
            self.event_list_url,
            {
                "name": "Demo Event Name",
                "contract": self.contract01.id,
            },
            format="json",
        )
        return resp

    # UPDATES

    def get_incoming_datetime_RIGHT_FORMAT(self):
        date = datetime.datetime.now() + datetime.timedelta(days=100)
        return date.strftime("%Y-%m-%d %H:%M:%S")

    def get_incoming_datetime_WRONG_FORMAT(self):
        date = datetime.datetime.now() + datetime.timedelta(days=100)
        return date.strftime("%Y-%m-%d")

    def helper_event_update_full(
        self,
        old_contract,
        new_contract,
        old_support_contact="sales1",
        new_support_contact="sales2",
        set_wrong_format=False,
    ):

        support_contact_id_old = self.profiles[old_support_contact]["instance"]

        if new_contract == "NOT_IN_DB":
            new_contract = 999
        else:
            new_contract = new_contract.id

        if new_support_contact == "NOT_IN_DB":
            support_contact_id_new = 999
        elif new_support_contact != "":
            support_contact_id_new = self.profiles[new_support_contact]["instance"].id

        event = Event.objects.create(
            name="Original name",
            contract=old_contract,
            support_contact=support_contact_id_old,
        )

        event.save()
        event_url = reverse(
            "client_contract_event",
            args=[self.client01.id, old_contract.id, event.id],
        )

        if set_wrong_format:
            incomingDate = self.get_incoming_datetime_WRONG_FORMAT()
        else:
            incomingDate = self.get_incoming_datetime_RIGHT_FORMAT()

        resp = self.client.put(
            event_url,
            {
                "name": "Demo Event Name",
                "contract": new_contract,
                "status": "CLOSED",
                "support_contact": support_contact_id_new,
                "attendees": 2000,
                "notes": "Bla bla bla",
                "start_date": incomingDate,
                "close_date": incomingDate,
            },
            format="json",
        )

        return resp

    def helper_event_update_min(self):

        event = Event.objects.create(
            name="Demo Event Name",
            contract=self.contract01,
            status="OPENED",
        )
        event.save()
        event_url = reverse(
            "client_contract_event",
            args=[self.client01.id, self.contract01.id, event.id],
        )

        resp = self.client.put(
            event_url,
            {
                "name": "Updated Demo Event Name",
                "contract": self.contract02.id,
            },
            format="json",
        )

        return resp

    def helper_event_update_no_name(self):

        event = Event.objects.create(
            name="Demo Event Name",
            contract=self.contract01,
        )
        event.save()
        event_url = reverse(
            "client_contract_event",
            args=[self.client01.id, self.contract01.id, event.id],
        )

        resp = self.client.put(
            event_url,
            {
                "contract": self.contract02.id,
            },
            format="json",
        )

        return resp

    def helper_event_update_no_contract(self):

        event = Event.objects.create(
            name="Demo Event Name",
            contract=self.contract01,
        )
        event.save()
        event_url = reverse(
            "client_contract_event",
            args=[self.client01.id, self.contract01.id, event.id],
        )

        resp = self.client.put(
            event_url,
            {
                "name": "Updated Demo Event Name",
            },
            format="json",
        )

        return resp

    def helper_event_update_no_data(self, old_support_contact="sales1"):

        event = Event.objects.create(
            name="Demo Event Name",
            contract=self.contract01,
        )
        event.save()
        event_url = reverse(
            "client_contract_event",
            args=[self.client01.id, self.contract01.id, event.id],
        )

        resp = self.client.put(
            event_url,
            {},
            format="json",
        )

        return resp

    # --- LIST EVENTS ---

    @printname
    def test_happy_events_list__MANAGE(self):
        self.login("manage1")
        resp = self.client.get(self.event_list_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_happy_events_list__SELL(self):
        self.login("sales1")
        resp = self.client.get(self.event_list_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_happy_events_list__SUPPORT(self):
        self.login("support1")
        resp = self.client.get(self.event_list_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_happy_events_list__NOTEAM(self):
        self.login("noteam")
        resp = self.client.get(self.event_list_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_sad_events_list__no_auth(self):
        resp = self.client.get(self.event_list_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- CREATE EVENTS ---

    @printname
    def test_happy_event_new__MANAGE_support_contact_is_NONE(self):
        resp = self.helper_event_new("manage1", self.contract01)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        event = Event.objects.get(id=resp.data["id"])
        self.assertEqual(None, event.support_contact)

    @printname
    def test_happy_event_new__MANAGE_support_contact_is_SET(self):
        resp = self.helper_event_new("manage1", self.contract01, "support2")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        event = Event.objects.get(id=resp.data["id"])
        self.assertEqual(self.profiles["support2"]["instance"], event.support_contact)

    @printname
    def test_happy_event_new__SELL__is_contract_owner(self):
        resp = self.helper_event_new("sales1", self.contract01, "")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        event = Event.objects.get(id=resp.data["id"])
        self.assertEqual(None, event.support_contact)

    @printname
    def test_sad_event_new__SELL__is_contract_owner_SET_support(self):
        resp = self.helper_event_new("sales1", self.contract01, "support2")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        event = Event.objects.get(id=resp.data["id"])
        self.assertEqual(
            None, event.support_contact
        )  # NOTE sales_team can't set support

    @printname
    def test_sad_event_new__SUPPORT(self):
        resp = self.helper_event_new("support1", self.contract01, "support2")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @printname
    def test_sad_event_new__NOTEAM(self):
        resp = self.helper_event_new("noteam", self.contract01, "support2")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @printname
    def test_happy_event_new_full__MANAGER(self):
        self.login("manage1")
        resp = self.helper_event_new_full()
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    @printname
    def test_happy_event_new_min(self):
        self.login("manage1")
        resp = self.helper_event_new_min()
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    @printname
    def test_happy_event_new_no_auth(self):
        resp = self.helper_event_new_min()
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    @printname
    def test_happy_event_new_no_data(self):
        self.login("manage1")
        resp = self.client.post(
            self.event_list_url,
            {},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    # --- FETCH EVENTS ---

    @printname
    def test_happy_event_fetch__MANAGE(self):
        event, event_url = self.helper_create_event()
        self.login("manage1")
        resp = self.client.get(event_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_happy_event_fetch__SELL(self):
        event, event_url = self.helper_create_event()
        self.login("sales1")
        resp = self.client.get(event_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_happy_event_fetch__SUPPORT(self):
        event, event_url = self.helper_create_event()
        self.login("support1")
        resp = self.client.get(event_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_happy_event_fetch__NOTEAM(self):
        event, event_url = self.helper_create_event()
        self.login("noteam")
        resp = self.client.get(event_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_sad_events_fetch_no_auth(self):
        event, event_url = self.helper_create_event()
        resp = self.client.get(event_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- UPDATE EVENTS ---

    @printname
    def test_happy_event_update_full__MANAGE(self):
        self.login("manage1")
        resp = self.helper_event_update_full(
            self.contract01, self.contract02, "support1", "support2"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_happy_event_update_full__SELL_owner_SAME_contract_CHANGE_support(self):
        self.login("sales1")
        resp = self.helper_event_update_full(
            self.contract01, self.contract01, "support1", "support2"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        event = Event.objects.get(id=resp.data["id"])
        self.assertEqual(
            self.profiles["support1"]["instance"], event.support_contact
        )  # NOTE not changed

    @printname
    def test_sad_event_update_full__SELL_owner_CHANGE_contract_SAME_support(self):
        self.login("sales1")
        resp = self.helper_event_update_full(
            self.contract01, self.contract02, "support1", "support1"
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @printname
    def test_happy_event_update_full__SELL_owner_CHANGE_contract_owned_CHANGE_support(
        self,
    ):
        self.login("sales1")
        resp = self.helper_event_update_full(
            self.contract01, self.contract03, "support1", "support2"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        event = Event.objects.get(id=resp.data["id"])
        self.assertEqual(self.contract03, event.contract)  # NOTE changed
        self.assertEqual(
            self.profiles["support1"]["instance"], event.support_contact
        )  # NOTE not changed

    @printname
    def test_happy_event_update_full__SUPPORT_owner_SAME_contract_SAME_support(self):
        self.login("support1")
        resp = self.helper_event_update_full(
            self.contract01, self.contract01, "support1", "support1"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_happy_event_update_full__SUPPORT_owner_CHANGE_contract_CHANGE_support(
        self,
    ):
        self.login("support1")
        resp = self.helper_event_update_full(
            self.contract01, self.contract02, "support1", "support2"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        event = Event.objects.get(id=resp.data["id"])
        self.assertEqual(self.contract01, event.contract)  # NOTE not changed
        self.assertEqual(
            self.profiles["support1"]["instance"], event.support_contact
        )  # NOTE not changed

    @printname
    def test_happy_event_update_full__SUPPORT_owner_SAME_contract_CHANGE_support(self):
        self.login("support1")
        resp = self.helper_event_update_full(
            self.contract01, self.contract01, "support1", "support2"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        event = Event.objects.get(id=resp.data["id"])
        self.assertEqual(
            self.profiles["support1"]["instance"], event.support_contact
        )  # NOTE not changed

    @printname
    def test_sad_event_update_full__NOTEAM(self):
        self.login("noteam")
        resp = self.helper_event_update_full(
            self.contract01, self.contract02, "support1", "support2"
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @printname
    def test_sad_event_update_full__NOTEAM_no_critical_change(self):
        self.login("noteam")
        resp = self.helper_event_update_full(
            self.contract01, self.contract01, "support1", "support1"
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    # Others on 1 profile that has the maximum permissions

    @printname
    def test_happy_event_update_min__MANAGE(self):
        self.login("manage1")
        resp = self.helper_event_update_min()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_happy_event_update_no_name__MANAGE(self):
        self.login("manage1")
        resp = self.helper_event_update_no_name()
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    @printname
    def test_happy_event_update_no_contract__MANAGE(self):
        self.login("manage1")
        resp = self.helper_event_update_no_contract()
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    @printname
    def test_happy_event_update_no_data__MANAGE(self):
        self.login("manage1")
        resp = self.helper_event_update_no_data()
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    @printname
    def test_happy_event_update_no_auth(self):
        resp = self.helper_event_update_min()
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- DELETE EVENTS ---

    @printname
    def test_happy_event_delete__MANAGE(self):
        event, event_url = self.helper_create_event()
        self.login("manage1")
        resp = self.client.delete(event_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    @printname
    def test_happy_event_delete__SELL__owner(self):
        event, event_url = self.helper_create_event(self.contract01)
        self.login("sales1")
        resp = self.client.delete(
            event_url, data={"format": "json"}
        )  # NOTE SAME sales_contact
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    @printname
    def test_happy_event_delete__SUPPORT(self):
        event, event_url = self.helper_create_event()
        self.login("support1")
        resp = self.client.delete(event_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @printname
    def test_happy_event_delete__NOTEAM(self):
        event, event_url = self.helper_create_event()
        self.login("noteam")
        resp = self.client.delete(event_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @printname
    def test_sad_event_delete_no_auth(self):
        event, event_url = self.helper_create_event()
        resp = self.client.delete(event_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- SALES_CONTACT ACT ON EVENT FOR WHICH HE ISN'T THE CURRENT SALES_CONTACT

    # CREATE
    @printname
    def test_sad_event_new__SELL__is_NOT_contract_owner(self):
        resp = self.helper_event_new("sales1", self.contract02)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    # FETCH
    @printname
    def test_happy_event_fetch__SELL_other(self):
        event, event_url = self.helper_create_event(self.contract02)
        self.login("sales1")
        resp = self.client.get(event_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    # UPDATE
    @printname
    def test_sad_event_update_full__SELL_other(self):
        self.login("sales1")
        resp = self.helper_event_update_full(
            self.contract02, self.contract01, "support1", "support2"
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @printname
    def test_sad_event_update_full__SUPPORT_other(self):
        self.login("support1")
        resp = self.helper_event_update_full(
            self.contract01, self.contract01, "support2", "support1"
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    # DELETE
    @printname
    def test_sad_event_delete__SELL__other(self):
        event, event_url = self.helper_create_event(self.contract02)
        self.login("sales1")
        resp = self.client.delete(event_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @printname
    def test_sad_event_delete__SUPPORT_other(self):
        event, event_url = self.helper_create_event()
        self.login("support2")
        resp = self.client.delete(event_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    # --- ACT ON NON EXISTING EVENT, CONTRACT OR USER ---

    # CREATE

    @printname
    def test_happy_event_new__MANAGE_contract_is_not_in_db(self):
        resp = self.helper_event_new("manage1", "NOT_IN_DB")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    @printname
    def test_happy_event_new__MANAGE_support_contact_is_not_in_db(self):
        resp = self.helper_event_new("manage1", self.contract01, "NOT_IN_DB")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    # FETCH
    @printname
    def test_sad_event_fetch__MANAGE(self):
        self.login("manage1")
        resp = self.client.get(self.event999_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    @printname
    def test_sad_event_fetch__SELL(self):
        self.login("sales1")
        resp = self.client.get(self.event999_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    @printname
    def test_sad_event_fetch__SUPPORT(self):
        self.login("support1")
        resp = self.client.get(self.event999_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    @printname
    def test_sad_event_fetch__NOTEAM(self):
        self.login("noteam")
        resp = self.client.get(self.event999_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    # UPDATE
    @printname
    def test_happy_event_update_full__MANAGE_not_in_db(self):
        self.login("manage1")
        resp = self.helper_event_update_full(
            self.contract01, "NOT_IN_DB", "support1", "support2"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    @printname
    def test_happy_event_update_full__MANAGE_support_not_in_db_other(self):
        self.login("manage1")
        resp = self.helper_event_update_full(
            self.contract01, self.contract02, "support1", "NOT_IN_DB"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    # DELETE
    @printname
    def test_sad_event_delete_not_in_db(self):
        event, event_url = self.helper_create_event()
        self.login("manage1")
        resp = self.client.delete(self.event999_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    # --- WRONG DATE FORMAT ---

    @printname
    def test_sad_event_new_full__MANAGER__WRONG_DATE_FORMAT(self):
        self.login("manage1")
        resp = self.helper_event_new_full(True)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    @printname
    def test_sad_event_update_full__MANAGE__WRONG_DATE_FORMAT(self):
        self.login("manage1")
        resp = self.helper_event_update_full(
            self.contract01, self.contract02, "support1", "support2", True
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
