from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from apps.users.models import EpicMember
from apps.crm.models import Client


def printname(function):
    def wrapper(*args, **kwargs):
        print(f"\n[{function.__name__}]", end="")
        return function(*args, **kwargs)

    return wrapper


class ClientsTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_url = reverse("token_obtain_pair")
        cls.client_list_url = reverse("clients")
        cls.client999_url = reverse("client", args=[999])

        cls.profiles = {
            "manage1": {
                "username": "demo_user_ma1",
                "email": "userma1@foo.com",
                "password": "demopass1",
                "team": EpicMember.Team.MANAGE,
            },
            "sales1": {
                "username": "demo_user_sa1",
                "email": "usersa1@foo.com",
                "password": "demopass1",
                "team": EpicMember.Team.SELL,
            },
            "sales2": {
                "username": "demo_user_sa2",
                "email": "usersa2@foo.com",
                "password": "demopass2",
                "team": EpicMember.Team.SELL,
            },
            "support1": {
                "username": "demo_user_su1",
                "email": "usersu1@foo.com",
                "password": "demopass1",
                "team": EpicMember.Team.SUPPORT,
            },
            "noteam": {
                "username": "demo_user_no1",
                "email": "userno1@foo.com",
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
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + self.token)

    def helper_create_client(self, old_sales_contact="sales1"):
        client = Client.objects.create(
            company_name="Client test",
            sales_contact=self.profiles[old_sales_contact]["instance"],
        )

        client.save()
        client_url = reverse("client", args=[client.id])

        return client, client_url

    # CREATES

    def helper_client_new(self, profile, sales_contact=""):
        self.login(profile)

        if sales_contact == "NOT_IN_DB":
            sales_contact = 999
        elif sales_contact != "":
            sales_contact = self.profiles[sales_contact]["instance"].id

        resp = self.client.post(
            self.client_list_url,
            {"company_name": "Test name", "sales_contact": sales_contact},
            format="json",
        )
        return resp

    def helper_client_new_full(self):
        resp = self.client.post(
            self.client_list_url,
            {
                "company_name": "Test company 123",
                "status": "PROSPECT",
                "sales_contact": self.profiles["sales2"]["instance"].id,
                "contact_first_name": "first name",
                "contact_last_name": "last name",
                "contact_email": "email@shedge.com",
                "contact_mobile": "0203040506",
                "company_phone": "0102030405",
            },
            format="json",
        )
        return resp

    def helper_client_new_min(self):
        resp = self.client.post(
            self.client_list_url,
            {"company_name": "Test company 123"},
            format="json",
        )
        return resp

    # UPDATES

    def helper_client_update_full(
        self, old_sales_contact="sales1", new_sales_contact="sales2"
    ):

        sales_contact_id_old = self.profiles[old_sales_contact]["instance"]

        if new_sales_contact == "NOT_IN_DB":
            sales_contact_id_new = 999
        elif new_sales_contact != "":
            sales_contact_id_new = self.profiles[new_sales_contact]["instance"].id

        client = Client.objects.create(
            company_name="Test company", sales_contact=sales_contact_id_old
        )
        client.save()
        client_url = reverse("client", args=[client.id])

        resp = self.client.put(
            client_url,
            {
                "company_name": "Test company 123 update",
                "status": "SIGNED",
                "sales_contact": sales_contact_id_new,
                "contact_first_name": "first name update",
                "contact_last_name": "last name update",
                "contact_email": "email@update.com",
                "contact_mobile": "0203040506 update",
                "company_phone": "0102030405 update",
            },
            format="json",
        )

        return resp

    def helper_client_update_min(self, old_sales_contact="sales1"):

        sales_contact_id_old = self.profiles[old_sales_contact]["instance"]

        client = Client.objects.create(
            company_name="Test company", sales_contact=sales_contact_id_old
        )
        client.save()
        client_url = reverse("client", args=[client.id])

        resp = self.client.put(
            client_url,
            {
                "company_name": "Test company 123 update",
            },
            format="json",
        )

        return resp

    def helper_client_update_no_company_name(
        self, old_sales_contact="sales1", new_sales_contact="sales1"
    ):

        sales_contact_id_old = self.profiles[old_sales_contact]["instance"]
        sales_contact_id_new = self.profiles[new_sales_contact]["instance"].id

        client = Client.objects.create(
            company_name="Test company", sales_contact=sales_contact_id_old
        )
        client.save()
        client_url = reverse("client", args=[client.id])
        sales_contact_id = sales_contact_id_new

        resp = self.client.put(
            client_url,
            {
                "status": "SIGNED",
                "sales_contact": sales_contact_id,
                "contact_first_name": "first name update",
                "contact_last_name": "last name update",
                "contact_email": "email@update.com",
                "contact_mobile": "0203040506 update",
                "company_phone": "0102030405 update",
            },
            format="json",
        )

        return resp

    def helper_client_update_no_data(self, old_sales_contact="sales1"):

        sales_contact_id_old = self.profiles[old_sales_contact]["instance"]

        client = Client.objects.create(
            company_name="Test company", sales_contact=sales_contact_id_old
        )
        client.save()
        client_url = reverse("client", args=[client.id])

        resp = self.client.put(
            client_url,
            {},
            format="json",
        )

        return resp

    # --- LIST CLIENTS ---

    @printname
    def test_happy_clients_list__MANAGE(self):
        self.login("manage1")
        resp = self.client.get(self.client_list_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_happy_clients_list__SELL(self):
        self.login("sales1")
        resp = self.client.get(self.client_list_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_happy_clients_list__SUPPORT(self):
        self.login("support1")
        resp = self.client.get(self.client_list_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_happy_clients_list__NOTEAM(self):
        self.login("noteam")
        resp = self.client.get(self.client_list_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_sad_clients_list__no_auth(self):
        resp = self.client.get(self.client_list_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- CREATE CLIENTS ---

    @printname
    def test_happy_client_new__MANAGE_sales_contact_NONE(self):
        resp = self.helper_client_new("manage1")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        client = Client.objects.get(id=resp.data["id"])
        self.assertEqual(None, client.sales_contact)

    @printname
    def test_happy_client_new__MANAGE_sales_contact_SET(self):
        resp = self.helper_client_new("manage1", "sales2")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        client = Client.objects.get(id=resp.data["id"])
        self.assertEqual(self.profiles["sales2"]["instance"], client.sales_contact)

    @printname
    def test_happy_client_new__SELL_owner(self):
        resp = self.helper_client_new("sales1")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        client = Client.objects.get(id=resp.data["id"])  # NOTE SAME sales_contact
        self.assertEqual(self.profiles["sales1"]["instance"], client.sales_contact)

    @printname
    def test_happy_client_new__SUPPORT(self):
        resp = self.helper_client_new("support1")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @printname
    def test_happy_client_new__NOTEAM(self):
        resp = self.helper_client_new("noteam")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @printname
    def test_happy_client_new_full__MANAGER(self):
        self.login("manage1")
        resp = self.helper_client_new_full()
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    @printname
    def test_happy_client_new_min(self):
        self.login("manage1")
        resp = self.helper_client_new_min()
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    @printname
    def test_happy_client_no_data(self):
        self.login("manage1")
        resp = self.client.post(
            self.client_list_url,
            {},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    @printname
    def test_happy_client_no_auth(self):
        resp = self.helper_client_new_min()
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- FETCH CLIENTS ---

    @printname
    def test_happy_client_fetch__MANAGE(self):
        client, client_url = self.helper_create_client()
        self.login("manage1")
        resp = self.client.get(client_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_happy_client_fetch__SELL(self):
        client, client_url = self.helper_create_client()
        self.login("sales1")
        resp = self.client.get(client_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_happy_client_fetch__SUPPORT(self):
        client, client_url = self.helper_create_client()
        self.login("support1")
        resp = self.client.get(client_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_happy_client_fetch__NOTEAM(self):
        client, client_url = self.helper_create_client()
        self.login("noteam")
        resp = self.client.get(client_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_sad_clients_fetch_no_auth(self):
        client, client_url = self.helper_create_client()
        resp = self.client.get(client_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- UPDATE CLIENTS ---

    @printname
    def test_happy_client_update_full__MANAGE(self):
        self.login("manage1")
        resp = self.helper_client_update_full("sales1", "sales2")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_happy_client_update_full__SELL(self):
        self.login("sales1")
        resp = self.helper_client_update_full(
            "sales1", "sales1"
        )  # NOTE SAME sales_contact
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_sad_client_update_full__SUPPORT(self):
        self.login("support1")
        resp = self.helper_client_update_full("sales1", "sales2")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @printname
    def test_sad_client_update_full__NOTEAM(self):
        self.login("noteam")
        resp = self.helper_client_update_full("sales1", "sales2")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    # Others on 1 profile that has the maximum permissions

    @printname
    def test_happy_client_update_min__MANAGE(self):
        self.login("manage1")
        resp = self.helper_client_update_min("sales1")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_happy_client_update_no_company_name__MANAGE(self):
        self.login("manage1")
        resp = self.helper_client_update_no_company_name("sales1", "sales1")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    @printname
    def test_happy_client_update_no_data__MANAGE(self):
        self.login("manage1")
        resp = self.helper_client_update_no_data("sales1")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    @printname
    def test_happy_client_update_no_auth(self):
        resp = self.helper_client_update_min("sales1")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- DELETE CLIENTS ---

    @printname
    def test_happy_client_delete__MANAGE(self):
        client, client_url = self.helper_create_client()
        self.login("manage1")
        resp = self.client.delete(client_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    @printname
    def test_happy_client_delete__SELL__owner(self):
        client, client_url = self.helper_create_client(old_sales_contact="sales1")
        self.login("sales1")
        resp = self.client.delete(
            client_url, data={"format": "json"}
        )  # NOTE SAME sales_contact
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    @printname
    def test_happy_client_delete__SUPPORT(self):
        client, client_url = self.helper_create_client()
        self.login("support1")
        resp = self.client.delete(client_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @printname
    def test_happy_client_delete__NOTEAM(self):
        client, client_url = self.helper_create_client()
        self.login("noteam")
        resp = self.client.delete(client_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @printname
    def test_sad_client_delete_no_auth(self):
        client, client_url = self.helper_create_client()
        resp = self.client.delete(client_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- SALES_CONTACT ACT ON A CLIENT ON WHICH HE ISN'T THE CURRENT SALES_CONTACT

    # CREATE
    @printname
    def test_happy_client_new__SELL_other(self):
        resp = self.helper_client_new(
            "sales1", "sales2"
        )  # NOTE DIFFERENT sales_contact
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        client = Client.objects.get(id=resp.data["id"])
        self.assertEqual(self.profiles["sales1"]["instance"], client.sales_contact)

    # FETCH
    @printname
    def test_happy_client_fetch__SELL_other(self):
        client, client_url = self.helper_create_client(
            "sales2"
        )  # NOTE DIFFERENT sales_contact
        self.login("sales1")
        resp = self.client.get(client_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    # UPDATE
    @printname
    def test_sad_client_update_full__SELL__other(self):
        self.login("sales1")
        resp = self.helper_client_update_full(
            "sales2", "sales1"
        )  # NOTE DIFFERENT sales_contact
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @printname
    def test_sad_client_update_full__SELL__owner(self):
        self.login("sales1")
        resp = self.helper_client_update_full(
            "sales1", "sales2"
        )  # NOTE DIFFERENT sales_contact
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        client = Client.objects.get(id=resp.data["id"])  # NOTE SAME sales_contact
        self.assertEqual(self.profiles["sales1"]["instance"], client.sales_contact)

    # DELETE
    @printname
    def test_sad_client_delete_SELL__other(self):
        client, client_url = self.helper_create_client(
            old_sales_contact="sales2"
        )  # NOTE DIFFERENT sales_contact
        self.login("sales1")
        resp = self.client.delete(client_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    # --- ACT ON NON EXISTING CLIENT OR USER ---

    # CREATE

    @printname
    def test_happy_client_new__MANAGE_sales_contact_NOT_IN_DB(self):
        resp = self.helper_client_new("manage1", "NOT_IN_DB")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    # FETCH

    @printname
    def test_sad_client_fetch_not_in_db__MANAGE(self):
        self.login("manage1")
        resp = self.client.get(self.client999_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    @printname
    def test_sad_client_fetch_not_in_db__SELL(self):
        self.login("sales1")
        resp = self.client.get(self.client999_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    @printname
    def test_sad_client_fetch_not_in_db__SUPPORT(self):
        self.login("support1")
        resp = self.client.get(self.client999_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    @printname
    def test_sad_client_fetch_not_in_db__NOTEAM(self):
        self.login("noteam")
        resp = self.client.get(self.client999_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    # UPDATE
    @printname
    def test_happy_client_update_not_in_db(self):
        self.login("manage1")

        resp = self.client.put(
            self.client999_url,
            {
                "company_name": "Test company 123 update",
            },
            format="json",
        )

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    @printname
    def test_happy_client_update_full__MANAGE__support_contact__not_in_db(self):
        self.login("manage1")
        resp = self.helper_client_update_full("sales1", "NOT_IN_DB")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    # DELETE
    @printname
    def test_sad_client_delete_not_in_db(self):
        self.login("manage1")
        resp = self.client.delete(self.client999_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
