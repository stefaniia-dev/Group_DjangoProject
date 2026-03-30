from django.contrib.auth import get_user, get_user_model
from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus
from django.contrib.auth.forms import AuthenticationForm
from .forms import CreateUserForm, LoginForm, CreateTaskForm, CreateListForm
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your tests here.
# To run tests do --> python manage.py test
# ------------- Log in tests ------------------
class LoginTestCase(TestCase):
    def setUp(self):
        self.username = "testing users"
        self.email = "useremail@gmail.com"
        self.password = "63ft44fyfuf4rb#%^&*ndndns"

        # creates a temporary user
        User.objects.create(
            username=self.username,
            email=self.email,
            password=self.password,
        )

    def test_loging_page_exists(self):
        response = self.client.get(reverse('log_in'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'log_in.html')

    def test_login_page_has_form(self):
        response = self.client.get(reverse('log_in'))
        form = response.context.get('form')
        self.assertIsInstance(form, AuthenticationForm)

    # def test_login_page(self):
    #     user_data = {'username': self.username,
    #                 'password': self.password
    #                  }
    #     response = self.client.post(reverse('log_in'),user_data)
    #     self.assertRedirects(response,'index/')








