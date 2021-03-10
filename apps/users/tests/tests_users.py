from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from apps.users.models import EpicMember


def printname(function):
    def wrapper(*args, **kwargs):
        print(f"\n[{function.__name__}]", end="")
        return function(*args, **kwargs)

    return wrapper


class EpicMembersTests(APITestCase):
    @classmethod
    def setUpClass(cls):

        cls.profiles = {
            "manage1": {
                "username": "em_demo_user_ma1",
                "email": "em_userma1@foo.com",
                "password": "demopass1",
                "team": EpicMember.Team.MANAGE,
            },
            "sales1": {
                "username": "em_demo_user_sa1",
                "email": "em_usersa1@foo.com",
                "password": "demopass1",
                "team": EpicMember.Team.SELL,
            },
            "support1": {
                "username": "em_demo_user_su1",
                "email": "em_usersu1@foo.com",
                "password": "demopass1",
                "team": EpicMember.Team.SUPPORT,
            },
            "noteam": {
                "username": "em_demo_user_no1",
                "email": "em_userno1@foo.com",
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
                profile["id"] = u.id

        cls.login_url = reverse("token_obtain_pair")
        # cls.signup_url = reverse("user_signup")
        cls.users_list_url = reverse("users_list")
        cls.user_manage1_details_url = reverse(
            "user_details", args=[cls.profiles["manage1"]["id"]]
        )
        cls.user_sales1_details_url = reverse(
            "user_details", args=[cls.profiles["sales1"]["id"]]
        )
        cls.user_support1_details_url = reverse(
            "user_details", args=[cls.profiles["support1"]["id"]]
        )
        cls.user_noteam_details_url = reverse(
            "user_details", args=[cls.profiles["noteam"]["id"]]
        )
        cls.user999_details_url = reverse("user_details", args=[999])

        cls.usercount = 0

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):

        u1 = EpicMember.objects.create_user(
            username="demo_user", email="user@foo.com", password="demopass"
        )

        u2 = EpicMember.objects.create_user(
            username="second_user", email="second_user@foo.com", password="demopass2"
        )

        u1.save()
        u2.save()

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

    def helper_get_user_details(self, profile):

        if profile == "NOT_IN_DB":
            user_id = 999
        else:
            user_id = self.profiles[profile]["id"]

        return reverse("user_details", args=[user_id])

    def helper_get_randname(self):
        self.usercount += 1
        return f"username{self.usercount}"

    def helper_user_create_full(self):

        resp = self.client.post(
            self.users_list_url,
            {
                "team": "SUPPORT",
                "username": self.helper_get_randname(),
                "first_name": "first name",
                "last_name:": "last name",
                "email": "updated@email.com",
                "password": "updated_password",
                "is_active": True,
            },
            format="json",
        )

        return resp

    def helper_user_create_min(self, with_user, with_pass):

        data = {}
        if with_user:
            data["username"] = self.helper_get_randname()
        if with_pass:
            data["password"] = "updated_password"

        resp = self.client.post(
            self.users_list_url,
            data,
            format="json",
        )

        return resp

    def helper_user_update_full(self, profile):
        resp = self.client.put(
            self.helper_get_user_details(profile),
            {
                "team": "SUPPORT",
                "username": self.helper_get_randname(),
                "first_name": "first name",
                "last_name:": "last name",
                "email": "updated@email.com",
                "password": "updated_password",
                "is_active": False,
            },
            format="json",
        )

        return resp

    def helper_user_update_min(self, profile):
        resp = self.client.put(
            self.helper_get_user_details(profile),
            {},
            format="json",
        )

        return resp

    # --- LOGIN / LOGOUT ---

    @printname
    def test_happy_login(self):
        resp = self.client.post(
            self.login_url,
            {"username": "demo_user_ma1", "password": "demopass1"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue("refresh" in resp.data)
        self.assertTrue("access" in resp.data)
        # token = resp.data["access"]
        # print(token)

    @printname
    def test_sad_login_wrong_username(self):
        resp = self.client.post(
            self.login_url,
            {"username": "demo_user_ma999", "password": "demopass1"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    @printname
    def test_sad_login_wrong_password(self):
        resp = self.client.post(
            self.login_url,
            {"username": "demo_user_ma1", "password": "wrongpass"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    @printname
    def test_sad_login_missing_username(self):
        resp = self.client.post(
            self.login_url, {"password": "demopass1"}, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    @printname
    def test_sad_login_missing_password(self):
        resp = self.client.post(
            self.login_url, {"username": "demo_user_ma1"}, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    @printname
    def test_sad_login_no_data(self):
        resp = self.client.post(self.login_url, {}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    # --- CREATE USERS ---

    @printname
    def test_happy_user_create_full__MANAGE(self):
        self.login("manage1")
        resp = self.helper_user_create_full()
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    @printname
    def test_happy_user_create_full__SELL(self):
        self.login("sales1")
        resp = self.helper_user_create_full()
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @printname
    def test_happy_user_create_full__SUPPORT(self):
        self.login("support1")
        resp = self.helper_user_create_full()
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @printname
    def test_happy_user_create_full__NO_TEAM(self):
        self.login("noteam")
        resp = self.helper_user_create_full()
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    # Others tests

    @printname
    def test_happy_user_create_min__MANAGE__NOTEAM(self):
        self.login("manage1")
        resp = self.helper_user_create_min(True, True)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    @printname
    def test_happy_user_create_no_username__MANAGE(self):
        self.login("manage1")
        resp = self.helper_user_create_min(False, True)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    @printname
    def test_happy_user_create_no_password__MANAGE(self):
        self.login("manage1")
        resp = self.helper_user_create_min(True, False)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    @printname
    def test_happy_user_create_no_data__MANAGE(self):
        self.login("manage1")
        resp = self.helper_user_create_min(False, False)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    @printname
    def test_sad_user_create_full__NO_AUTH(self):
        resp = self.helper_user_create_full()
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- LIST USERS ---

    @printname
    def test_happy_users_list__MANAGE(self):
        self.login("manage1")
        resp = self.client.get(self.users_list_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_happy_users_list__SELL(self):
        self.login("sales1")
        resp = self.client.get(self.users_list_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)  # NOTE really ?

    @printname
    def test_happy_users_list__SUPPORT(self):
        self.login("support1")
        resp = self.client.get(self.users_list_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)  # NOTE really ?

    @printname
    def test_happy_users_list__NO_TEAM(self):
        self.login("noteam")
        resp = self.client.get(self.users_list_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)  # NOTE really ?

    @printname
    def test_sad_users_list__NO_AUTH(self):
        resp = self.client.get(self.users_list_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- FETCH USER ---

    @printname
    def test_happy_user_fetch__MANAGE__MANAGE(self):
        self.login("manage1")
        resp = self.client.get(self.user_manage1_details_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_happy_user_fetch__SELL__SELL(self):
        self.login("sales1")
        resp = self.client.get(self.user_sales1_details_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_sad_user_fetch__SUPPORT__SUPPORT(self):
        self.login("support1")
        resp = self.client.get(self.user_support1_details_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_sad_user_fetch__NO_TEAM__NO_TEAM(self):
        self.login("noteam")
        resp = self.client.get(self.user_noteam_details_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_sad_user_fetch__NO_AUTH(self):
        resp = self.client.get(
            self.helper_get_user_details("manage1"), data={"format": "json"}
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- UPDATE USER ---

    @printname
    def test_happy_user_update_full__MANAGE(self):
        self.login("manage1")
        resp = self.helper_user_update_full("manage1")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_happy_user_update_full__SELL(self):
        self.login("sales1")
        resp = self.helper_user_update_full("sales1")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_happy_user_update_full__SUPPORT(self):
        self.login("support1")
        resp = self.helper_user_update_full("support1")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_happy_user_update_full__NO_TEAM(self):
        self.login("noteam")
        resp = self.helper_user_update_full("noteam")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    # Others tests

    @printname
    def test_happy_user_update_min__MANAGE__NOTEAM(self):
        self.login("manage1")
        resp = self.helper_user_update_min("noteam")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_happy_user_update_no_data__MANAGE(self):
        self.login("manage1")
        resp = self.helper_user_update_min("noteam")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_sad_user_update_full__NO_AUTH(self):
        resp = self.helper_user_update_full("manage1")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- DELETE USER ---

    @printname
    def test_happy_user_delete__MANAGE(self):
        self.login("manage1")
        resp = self.client.delete(
            self.user_manage1_details_url, data={"format": "json"}
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)  # NOTE Really ?

    @printname
    def test_happy_user_delete__SELL(self):
        self.login("sales1")
        resp = self.client.delete(self.user_sales1_details_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @printname
    def test_happy_user_delete__SUPPORT(self):
        self.login("support1")
        resp = self.client.delete(
            self.user_support1_details_url, data={"format": "json"}
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @printname
    def test_happy_user_delete__NOTEAM(self):
        self.login("noteam")
        resp = self.client.delete(self.user_noteam_details_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    # Others

    @printname
    def test_sad_users_delete_NO_AUTH(self):
        resp = self.client.delete(
            self.user_manage1_details_url, data={"format": "json"}
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- ACT ON SOMEONE ELSE PROFILE ---

    # FETCH MANAGE Others

    @printname
    def test_happy_user_fetch__MANAGE__SELL(self):
        self.login("manage1")
        resp = self.client.get(self.user_sales1_details_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_happy_user_fetch__MANAGE__SUPPORT(self):
        self.login("manage1")
        resp = self.client.get(self.user_support1_details_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_happy_user_fetch__MANAGE__NO_TEAM(self):
        self.login("manage1")
        resp = self.client.get(self.user_noteam_details_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    # FETCH SELL Others

    @printname
    def test_sad_user_fetch__SELL__MANAGE(self):
        self.login("sales1")
        resp = self.client.get(self.user_manage1_details_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @printname
    def test_sad_user_fetch__SELL__SUPPORT(self):
        self.login("sales1")
        resp = self.client.get(self.user_support1_details_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @printname
    def test_sad_user_fetch__SELL__NO_TEAM(self):
        self.login("sales1")
        resp = self.client.get(self.user_noteam_details_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    # FETCH SUPPORT Others

    @printname
    def test_sad_user_fetch__SUPPORT__MANAGE(self):
        self.login("support1")
        resp = self.client.get(self.user_manage1_details_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @printname
    def test_happy_user_fetch__SUPPORT__SELL(self):
        self.login("support1")
        resp = self.client.get(self.user_sales1_details_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @printname
    def test_sad_user_fetch__SUPPORT__NO_TEAM(self):
        self.login("support1")
        resp = self.client.get(self.user_noteam_details_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    # FETCH NOTEAM Others

    @printname
    def test_sad_user_fetch__NO_TEAM__MANAGE(self):
        self.login("noteam")
        resp = self.client.get(self.user_manage1_details_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @printname
    def test_happy_user_fetch__NO_TEAM__SELL(self):
        self.login("noteam")
        resp = self.client.get(self.user_sales1_details_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @printname
    def test_sad_user_fetch__NO_TEAM__SUPPORT(self):
        self.login("noteam")
        resp = self.client.get(self.user_support1_details_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    # UPDATE MANAGE Others

    @printname
    def test_happy_user_update_full__MANAGE__SELL(self):
        self.login("manage1")
        resp = self.helper_user_update_full("sales1")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_happy_user_update_full__MANAGE__SUPPORT(self):
        self.login("manage1")
        resp = self.helper_user_update_full("support1")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_happy_user_update_full__MANAGE__NO_TEAM(self):
        self.login("manage1")
        resp = self.helper_user_update_full("noteam")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    # UPDATE others others (partial)

    @printname
    def test_sad_user_update_full__SELL__MANAGE(self):
        self.login("sales1")
        resp = self.helper_user_update_full("manage1")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @printname
    def test_sad_user_update_full__SUPPORT__MANAGE(self):
        self.login("support1")
        resp = self.helper_user_update_full("manage1")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @printname
    def test_sad_user_update_full__NO_TEAM__MANAGE(self):
        self.login("noteam")
        resp = self.helper_user_update_full("manage1")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    # DELETE MANAGE Others

    @printname
    def test_happy_user_delete__MANAGE__SELL(self):
        self.login("manage1")
        resp = self.client.delete(
            self.helper_get_user_details("sales1"), data={"format": "json"}
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    @printname
    def test_happy_user_delete__MANAGE__SUPPORT(self):
        self.login("manage1")
        resp = self.client.delete(
            self.helper_get_user_details("support1"), data={"format": "json"}
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    @printname
    def test_happy_user_delete__MANAGE__NOTEAM(self):
        self.login("manage1")
        resp = self.client.delete(
            self.helper_get_user_details("noteam"), data={"format": "json"}
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    # DELETE Others others (partial)

    @printname
    def test_sad_user_delete__SELL__MANAGE(self):
        self.login("sales1")
        resp = self.client.delete(
            self.helper_get_user_details("manage1"), data={"format": "json"}
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @printname
    def test_sad_user_delete__SELL__NOTEAM(self):
        self.login("sales1")
        resp = self.client.delete(
            self.helper_get_user_details("noteam"), data={"format": "json"}
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @printname
    def test_sad_user_delete__SUPPORT__MANAGE(self):
        self.login("support1")
        resp = self.client.delete(
            self.helper_get_user_details("manage1"), data={"format": "json"}
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @printname
    def test_sad_user_delete__SUPPORT__NOTEAM(self):
        self.login("support1")
        resp = self.client.delete(
            self.helper_get_user_details("noteam"), data={"format": "json"}
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @printname
    def test_sad_user_delete__NOTEAM__MANAGE(self):
        self.login("noteam")
        resp = self.client.delete(
            self.helper_get_user_details("manage1"), data={"format": "json"}
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @printname
    def test_sad_user_delete__NOTEAM__SELL(self):
        self.login("noteam")
        resp = self.client.delete(
            self.helper_get_user_details("sales1"), data={"format": "json"}
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    # # --- ACT ON NON EXISTING PROFILE ---

    # FETCH
    @printname
    def test_sad_user_fetch_not_in_db(self):
        self.login("manage1")
        resp = self.client.get(self.user999_details_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    # UPDATE
    @printname
    def test_sad_user_update_full__MANAGE(self):
        self.login("manage1")
        resp = self.helper_user_update_full("NOT_IN_DB")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    # DELETE
    @printname
    def test_sad_user_delete_not_in_db(self):
        self.login("manage1")
        resp = self.client.delete(self.user999_details_url, data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
