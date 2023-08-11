from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import CustomUser


class AccountTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        account = CustomUser.objects.create_user(
            "tester", "tester@gmail.com", password="pass"
        )
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(account.username, "tester")
        self.assertTrue(account.check_password("pass"))


# class AccountsTest(APITestCase):
#     def test_authentication(self):
#         User = get_user_model()
#         self.client.login(username="temp", password="temp")
#         response = self.client.get
