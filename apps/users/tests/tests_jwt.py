from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from apps.users.models import EpicMember


def printname(function):
    def wrapper(*args, **kwargs):
        print(f"\n[{function.__name__}]", end="")
        return function(*args, **kwargs)

    return wrapper


class JwtTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.url = reverse("token_obtain_pair")
        cls.verification_url = reverse("token_verify")
        cls.client = APIClient()

        u = EpicMember.objects.create_user(
            username="demo_user_jwt", email="user_jwt@foo.com", password="demopass"
        )
        u.save()

    @classmethod
    def tearDownClass(cls):
        pass

    def get_access(self):
        resp = self.client.post(
            self.url,
            {"username": "demo_user_jwt", "password": "demopass"},
            format="json",
        )
        return resp, resp.data["access"]
        # print(token)

    # --- TESTS ---

    @printname
    def test_sad_invalid_user(self):
        resp = self.client.post(
            self.url,
            {"username": "demo_user_jwt", "password": "wrongpass"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    @printname
    def test_happy_valid_user(self):
        resp, token = self.get_access()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue("refresh" in resp.data)
        self.assertTrue("access" in resp.data)

    @printname
    def test_sad_wrong_token_verification(self):
        resp = self.client.post(self.verification_url, {"token": "abc"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    @printname
    def test_happy_right_token_verification(self):
        access_resp, token = self.get_access()
        resp = self.client.post(self.verification_url, {"token": token}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @printname
    def test_sad_wrong_token_access(self):
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + "abc")
        resp = self.client.get("/clients/", data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    @printname
    def test_happy_right_token_access(self):
        access_resp, token = self.get_access()
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + token)
        resp = self.client.get("/clients/", data={"format": "json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
