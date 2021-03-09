import datetime

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from apps.users.models import EpicMember
from apps.crm.models import Client, Contract


def printname(function):
    def wrapper(*args, **kwargs):
        print(f"\n[{function.__name__}]", end="")
        return function(*args, **kwargs)

    return wrapper


class ContractsTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_url = reverse("token_obtain_pair")

        cls.profiles = {
            "manage1": {
                "username": "cli_demo_user_ma1",
                "email": "cli_userma1@foo.com",
                "password": "demopass1",
                "team": EpicMember.Team.MANAGE,
            },
            "sales1": {
                "username": "cli_demo_user_sa1",
                "email": "cli_usersa1@foo.com",
                "password": "demopass1",
                "team": EpicMember.Team.SELL,
            },
            "sales2": {
                "username": "cli_demo_user_sa2",
                "email": "cli_usersa2@foo.com",
                "password": "demopass2",
                "team": EpicMember.Team.SELL,
            },
            "support1": {
                "username": "cli_demo_user_su1",
                "email": "cli_usersu1@foo.com",
                "password": "demopass1",
                "team": EpicMember.Team.SUPPORT,
            },
            "noteam": {
                "username": "cli_demo_user_no1",
                "email": "cli_userno1@foo.com",
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

        cls.client02 = Client.objects.create(
            company_name="Contract test 02",
            sales_contact=cls.profiles["sales2"]["instance"],
        )

        cls.client02.save()
        cls.client02_url = reverse("client", args=[cls.client02.id])

        cls.contract_list_url = reverse("client_contracts", args=[cls.client01.id])
        cls.contract999_url = reverse("client_contract", args=[cls.client01.id, 999])

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

    def helper_create_contract(self, old_sales_contact="sales1"):
        contract = Contract.objects.create(
            client=self.client01,
            sales_contact=self.profiles[old_sales_contact]["instance"],
        )

        contract.save()
        contract_url = reverse("client_contract", args=[self.client01.id, contract.id])

        return contract, contract_url

    # CREATES

    def helper_contract_new(self, profile, new_client, sales_contact=""):
        self.login(profile)

        if sales_contact == "NOT_IN_DB":
            sales_contact = 999
        elif sales_contact != "":
            sales_contact = self.profiles[sales_contact]["instance"].id

        if new_client == "NOT_IN_DB":
            client_id = 999
        else:
            client_id = new_client.id

        resp = self.client.post(
            self.contract_list_url,
            {"client": client_id, "sales_contact": sales_contact},
            format="json",
        )

        return resp

    def helper_contract_new_full(self, set_wrong_format=False):

        if set_wrong_format:
            paydate = self.get_incoming_date_WRONG_FORMAT()
        else:
            paydate = self.get_incoming_date_RIGHT_FORMAT()

        resp = self.client.post(
            self.contract_list_url,
            {
                "client": self.client01.id,
                "sales_contact": self.profiles["sales2"]["instance"].id,
                "status": "SIGNED",
                "amount": 15000.0,
                "payment_date": paydate,
            },
            format="json",
        )

        return resp

    def helper_contract_new_min(self):
        resp = self.client.post(
            self.contract_list_url,
            {"client": self.client01.id},
            format="json",
        )
        return resp

    # UPDATES

    def get_incoming_date_RIGHT_FORMAT(self):
        date = datetime.datetime.now() + datetime.timedelta(days=100)
        return date.strftime("%Y-%m-%d")

    def get_incoming_date_WRONG_FORMAT(self):
        date = datetime.datetime.now() + datetime.timedelta(days=100)
        return date.strftime("%Y-%m-%d %H:%M:%s")

    def helper_contract_update_full(
        self,
        old_sales_contact="sales1",
        new_sales_contact="sales2",
        set_wrong_format=False,
    ):

        sales_contact_id_old = self.profiles[old_sales_contact]["instance"]

        if new_sales_contact == "NOT_IN_DB":
            sales_contact_id_new = 999
        elif new_sales_contact != "":
            sales_contact_id_new = self.profiles[new_sales_contact]["instance"].id

        contract = Contract.objects.create(
            client=self.client01, sales_contact=sales_contact_id_old
        )
        contract.save()
        contract_url = reverse("client_contract", args=[self.client01.id, contract.id])

        if set_wrong_format:
            paydate = self.get_incoming_date_WRONG_FORMAT()
        else:
            paydate = self.get_incoming_date_RIGHT_FORMAT()

        resp = self.client.put(
            contract_url,
            {
                "client": self.client02.id,
                "sales_contact": sales_contact_id_new,
                "status": "SIGNED",
                "amount": 15000.0,
                "payment_date": paydate,
            },
            format="json",
        )

        return resp

    def helper_contract_update_min(self, old_sales_contact="sales1"):

        sales_contact_id_old = self.profiles[old_sales_contact]["instance"]

        contract = Contract.objects.create(
            client=self.client01, sales_contact=sales_contact_id_old
        )
        contract.save()
        contract_url = reverse("client_contract", args=[self.client01.id, contract.id])

        resp = self.client.put(
            contract_url,
            {
                "client": self.client02.id,
            },
            format="json",
        )

        return resp

    def helper_contract_update_no_client(
        self, old_sales_contact="sales1", new_sales_contact="sales2"
    ):

        sales_contact_id_old = self.profiles[old_sales_contact]["instance"]
        sales_contact_id_new = self.profiles[new_sales_contact]["instance"].id

        contract = Contract.objects.create(
            client=self.client01, sales_contact=sales_contact_id_old
        )
        contract.save()
        contract_url = reverse("client_contract", args=[self.client01.id, contract.id])

        resp = self.client.put(
            contract_url,
            {
                "sales_contact": sales_contact_id_new,
                "status": "SIGNED",
                "amount": 15000.0,
                "payment_date": self.get_incoming_date_RIGHT_FORMAT(),
            },
            format="json",
        )

        return resp

    def helper_contract_update_no_data(self, old_sales_contact="sales1"):

        sales_contact_id_old = self.profiles[old_sales_contact]["instance"]

        contract = Contract.objects.create(
            client=self.client01, sales_contact=sales_contact_id_old
        )
        contract.save()
        contract_url = reverse("client_contract", args=[self.client01.id, contract.id])

        resp = self.client.put(
            contract_url,
            {},
            format="json",
        )

        return resp

    # --- LIST CONTRACTS ---

    @printname
    def test_happy_contracts_list__MANAGE(self):
        self.login("manage1")
        resp = self.client.get(self.contract_list_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_happy_contracts_list__SELL(self):
        self.login("sales1")
        resp = self.client.get(self.contract_list_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_happy_contracts_list__SUPPORT(self):
        self.login("support1")
        resp = self.client.get(self.contract_list_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_happy_contracts_list__NOTEAM(self):
        self.login("noteam")
        resp = self.client.get(self.contract_list_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_sad_contracts_list__no_auth(self):
        resp = self.client.get(self.contract_list_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- CREATE CONTRACTS ---

    @printname
    def test_happy_contract_new__MANAGE_sales_contact_is_NONE(self):
        resp = self.helper_contract_new("manage1", self.client01)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        contract = Contract.objects.get(id=resp.data["id"])
        self.assertEqual(None, contract.sales_contact)

    @printname
    def test_happy_contract_new__MANAGE_sales_contact_is_SET(self):
        resp = self.helper_contract_new("manage1", self.client01, "sales2")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        contract = Contract.objects.get(id=resp.data["id"])
        self.assertEqual(self.profiles["sales2"]["instance"], contract.sales_contact)

    @printname
    def test_happy_contract_new__SELL_owner(self):
        resp = self.helper_contract_new("sales1", self.client01, "sales1")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        contract = Contract.objects.get(id=resp.data["id"])  # NOTE SAME sales_contact
        self.assertEqual(self.profiles["sales1"]["instance"], contract.sales_contact)

    @printname
    def test_happy_contract_new__SUPPORT(self):
        resp = self.helper_contract_new("support1", self.client01)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @printname
    def test_happy_contract_new__NOTEAM(self):
        resp = self.helper_contract_new("noteam", self.client01)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @printname
    def test_happy_contract_new_full__MANAGER(self):
        self.login("manage1")
        resp = self.helper_contract_new_full()
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    @printname
    def test_happy_contract_new_min(self):
        self.login("manage1")
        resp = self.helper_contract_new_min()
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    @printname
    def test_happy_contract_no_auth(self):
        resp = self.helper_contract_new_min()
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    @printname
    def test_happy_contract_no_data(self):
        self.login("manage1")
        resp = self.client.post(
            self.contract_list_url,
            {},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    # --- FETCH CONTRACTS ---

    @printname
    def test_happy_contract_fetch__MANAGE(self):
        contract, contract_url = self.helper_create_contract()
        self.login("manage1")
        resp = self.client.get(contract_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_happy_contract_fetch__SELL(self):
        contract, contract_url = self.helper_create_contract()
        self.login("sales1")
        resp = self.client.get(contract_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_happy_contract_fetch__SUPPORT(self):
        contract, contract_url = self.helper_create_contract()
        self.login("support1")
        resp = self.client.get(contract_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_happy_contract_fetch__NOTEAM(self):
        contract, contract_url = self.helper_create_contract()
        self.login("noteam")
        resp = self.client.get(contract_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_sad_contracts_fetch_no_auth(self):
        contract, contract_url = self.helper_create_contract()
        resp = self.client.get(contract_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- UPDATE CONTRACTS ---

    @printname
    def test_happy_contract_update_full__MANAGE(self):
        self.login("manage1")
        resp = self.helper_contract_update_full("sales1", "sales2")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_happy_contract_update_full__SELL(self):
        self.login("sales1")
        resp = self.helper_contract_update_full(
            "sales1", "sales1"
        )  # NOTE SAME sales_contact
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_sad_contract_update_full__SUPPORT(self):
        self.login("support1")
        resp = self.helper_contract_update_full("sales1", "sales2")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @printname
    def test_sad_contract_update_full__NOTEAM(self):
        self.login("noteam")
        resp = self.helper_contract_update_full("sales1", "sales2")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    # Others on 1 profile that has the maximum permissions

    @printname
    def test_happy_contract_update_min__MANAGE(self):
        self.login("manage1")
        resp = self.helper_contract_update_min()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_happy_contract_update_no_company_name__MANAGE(self):
        self.login("manage1")
        resp = self.helper_contract_update_no_client()
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    @printname
    def test_happy_contract_update_no_data__MANAGE(self):
        self.login("manage1")
        resp = self.helper_contract_update_no_data()
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    @printname
    def test_happy_contract_update_no_auth(self):
        resp = self.helper_contract_update_min()
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- DELETE CONTRACTS ---

    @printname
    def test_happy_contract_delete__MANAGE(self):
        contract, contract_url = self.helper_create_contract()
        self.login("manage1")
        resp = self.client.delete(contract_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    @printname
    def test_happy_contract_delete__SELL__owner(self):
        contract, contract_url = self.helper_create_contract(old_sales_contact="sales1")
        self.login("sales1")
        resp = self.client.delete(
            contract_url, data={"format": "json"}
        )  # NOTE SAME sales_contact
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    @printname
    def test_happy_contract_delete__SUPPORT(self):
        contract, contract_url = self.helper_create_contract()
        self.login("support1")
        resp = self.client.delete(contract_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @printname
    def test_happy_contract_delete__NOTEAM(self):
        contract, contract_url = self.helper_create_contract()
        self.login("noteam")
        resp = self.client.delete(contract_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @printname
    def test_sad_contract_delete_no_auth(self):
        contract, contract_url = self.helper_create_contract()
        resp = self.client.delete(contract_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- SALES_CONTACT ACT ON A CONTRACT ON WHICH HE ISN'T THE CURRENT SALES_CONTACT

    # CREATE
    @printname
    def test_happy_contract_new__SELL_other(self):
        resp = self.helper_contract_new(
            "sales1", self.client01, "sales2"
        )  # NOTE DIFFERENT sales_contact
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        contract = Contract.objects.get(id=resp.data["id"])
        self.assertEqual(self.profiles["sales1"]["instance"], contract.sales_contact)

    # FETCH
    @printname
    def test_happy_contract_fetch__SELL_other(self):
        contract, contract_url = self.helper_create_contract(
            "sales2"
        )  # NOTE DIFFERENT sales_contact
        self.login("sales1")
        resp = self.client.get(contract_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    # UPDATE
    @printname
    def test_sad_contract_update_full__SELL__other(self):
        self.login("sales1")
        resp = self.helper_contract_update_full(
            "sales2", "sales1"
        )  # NOTE DIFFERENT sales_contact
        self.assertEqual(
            resp.status_code, status.HTTP_403_FORBIDDEN
        )  # TODO 200 avec sales_contact == sales1 ?

    @printname
    def test_sad_contract_update_full__SELL__owner(self):
        self.login("sales1")
        resp = self.helper_contract_update_full(
            "sales1", "sales2"
        )  # NOTE DIFFERENT sales_contact
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        contract = Contract.objects.get(id=resp.data["id"])  # NOTE SAME sales_contact
        self.assertEqual(self.profiles["sales1"]["instance"], contract.sales_contact)

    # DELETE
    @printname
    def test_sad_contract_delete_SELL__other(self):
        contract, contract_url = self.helper_create_contract(
            old_sales_contact="sales2"
        )  # NOTE DIFFERENT sales_contact
        self.login("sales1")
        resp = self.client.delete(contract_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    # --- ACT ON NON EXISTING CONTRACT OR USER ---

    # CREATE

    @printname
    def test_happy_contract_new__MANAGE_sales_contact_NOT_IN_DB(self):
        resp = self.helper_contract_new("manage1", self.client01, "NOT_IN_DB")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    @printname
    def test_happy_contract_new__MANAGE__NOT_A_CLIENT(self):
        resp = self.helper_contract_new("manage1", "NOT_IN_DB", "sales1")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    # FETCH

    @printname
    def test_sad_contract_fetch_not_in_db__MANAGE(self):
        self.login("manage1")
        resp = self.client.get(self.contract999_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    @printname
    def test_sad_contract_fetch_not_in_db__SELL(self):
        self.login("sales1")
        resp = self.client.get(self.contract999_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    @printname
    def test_sad_contract_fetch_not_in_db__SUPPORT(self):
        self.login("support1")
        resp = self.client.get(self.contract999_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    @printname
    def test_sad_contract_fetch_not_in_db__NOTEAM(self):
        self.login("noteam")
        resp = self.client.get(self.contract999_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    # UPDATE
    @printname
    def test_happy_contract_update_not_in_db(self):
        self.login("manage1")

        resp = self.client.put(
            self.contract999_url,
            {"client": self.client01.id},
            format="json",
        )

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    @printname
    def test_happy_contract_update_full__MANAGE__support_contact__not_in_db(self):
        self.login("manage1")
        resp = self.helper_contract_update_full("sales1", "NOT_IN_DB")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    # DELETE
    @printname
    def test_sad_contract_delete_not_in_db(self):
        self.login("manage1")
        resp = self.client.delete(self.contract999_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    # --- WRONG DATE FORMAT ---

    @printname
    def test_happy_contract_new_full__MANAGER__WRONG_DATE_FORMAT(self):
        self.login("manage1")
        resp = self.helper_contract_new_full(True)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    @printname
    def test_happy_contract_update_full__MANAGE__WRONG_DATE_FORMAT(self):
        self.login("manage1")
        resp = self.helper_contract_update_full("sales1", "sales2", True)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
