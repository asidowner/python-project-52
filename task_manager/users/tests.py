from collections import OrderedDict

from django.contrib.auth import models as auth_models
from django.template.response import TemplateResponse
from django.test import TestCase, Client
from django.urls import reverse_lazy
from faker import Faker
from faker.generator import Generator

from task_manager.users.forms import UserCreateForm


# ToDo Подумать как привязать к AbstractCRUDTest
class RegistrationPageViewTest(TestCase):

    def setUp(self) -> None:
        self.client: Client = Client()

    def test(self):
        response: TemplateResponse = self.client.get(
            reverse_lazy('users:create'),
        )
        form_fields: OrderedDict = UserCreateForm.base_fields
        self._assert_first_name(form_fields, response)
        self._assert_last_name(form_fields, response)
        self._assert_username(form_fields, response)
        self._assert_password(form_fields, response)
        self._assert_password_confirmation(form_fields, response)

    def _assert_first_name(self,
                           form_fields: OrderedDict,
                           response: TemplateResponse):
        self.assertIn(
            str(form_fields['first_name'].label),
            response.rendered_content,
        )
        self.assertIn(
            str(form_fields['first_name'].help_text),
            response.rendered_content,
        )

    def _assert_last_name(self,
                          form_fields: OrderedDict,
                          response: TemplateResponse):
        self.assertIn(
            str(form_fields['last_name'].label),
            response.rendered_content,
        )
        self.assertIn(
            str(form_fields['last_name'].help_text),
            response.rendered_content,
        )

    def _assert_username(self,
                         form_fields: OrderedDict,
                         response: TemplateResponse):
        self.assertIn(
            str(form_fields['username'].label),
            response.rendered_content,
        )
        self.assertIn(
            str(form_fields['username'].help_text),
            response.rendered_content,
        )

    def _assert_password(self,
                         form_fields: OrderedDict,
                         response: TemplateResponse):
        self.assertIn(
            str(form_fields['password1'].label),
            response.rendered_content,
        )
        self.assertIn(
            str(form_fields['password1'].help_text),
            response.rendered_content,
        )

    def _assert_password_confirmation(self,
                                      form_fields: OrderedDict,
                                      response: TemplateResponse):
        self.assertIn(
            str(form_fields['password2'].label),
            response.rendered_content,
        )
        self.assertIn(
            str(form_fields['password2'].help_text),
            response.rendered_content,
        )


class UsersTest(TestCase):
    """Test user registration."""

    def setUp(self):
        """Create a test database."""
        self.client: Client = Client()
        self.faker: Generator = Faker()

    def test_success_registration(self):
        response: TemplateResponse = self._send_request_registration()
        self.assertRedirects(response, reverse_lazy('auth:login'))
        self.assertTrue(
            auth_models.User.objects.filter(first_name=self._first_name,
                                            last_name=self._last_name,
                                            username=self._user_name),
        )

    def test_success_change_user_data(self):
        self._make_login()
        user: auth_models.User = self._get_user_db()
        new_first_name: str = self.faker.first_name()
        new_last_name: str = self.faker.last_name()
        new_user_name: str = self.faker.user_name()
        response: TemplateResponse = self.client.post(
            reverse_lazy('users:update', kwargs={'pk': user.id}),
            data={
                'first_name': new_first_name,
                'last_name': new_last_name,
                'username': new_user_name,
                'password1': self._fake_password,
                'password2': self._fake_password,
            },
        )
        self.assertRedirects(response, reverse_lazy('users:list'))
        self.assertTrue(
            auth_models.User.objects.filter(first_name=new_first_name,
                                            last_name=new_last_name,
                                            username=new_user_name),
        )

    def test_success_delete_user_data(self):
        self._make_login()
        user: auth_models.User = self._get_user_db()
        response: TemplateResponse = self.client.post(
            reverse_lazy('users:delete', kwargs={'pk': user.id}),
        )
        self.assertRedirects(response, reverse_lazy('users:list'))
        self.assertFalse(
            auth_models.User.objects.filter(first_name=self._first_name,
                                            last_name=self._last_name,
                                            username=self._user_name),
        )

    def _make_login(self):
        self._send_request_registration()
        self.client.login(username=self._user_name,
                          password=self._fake_password)

    def _send_request_registration(self) -> TemplateResponse:
        self._generate_user_data()
        response: TemplateResponse = self.client.post(
            reverse_lazy('users:create'),
            data={
                'first_name': self._first_name,
                'last_name': self._last_name,
                'username': self._user_name,
                'password1': self._fake_password,
                'password2': self._fake_password,
            },
        )
        return response

    def _generate_user_data(self) -> None:
        self._first_name: str = self.faker.first_name()
        self._last_name: str = self.faker.last_name()
        self._fake_password: str = self.faker.password(length=10)
        self._user_name: str = self.faker.user_name()

    def _get_user_db(self) -> auth_models.User:
        return auth_models.User.objects.filter(first_name=self._first_name,
                                               last_name=self._last_name,
                                               username=self._user_name).first()
