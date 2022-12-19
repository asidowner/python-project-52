from django.template.response import TemplateResponse
from django.test import TestCase, Client
from django.urls import reverse_lazy
from faker import Faker
from faker.generator import Generator


class LoginTest(TestCase):
    """Test user registration."""

    def setUp(self):
        """Create a test database."""
        self.client: Client = Client()
        self.faker: Generator = Faker()

    def test(self):
        self._send_request_registration()
        self.assertTrue(self.client.login(username=self._user_name,
                                          password=self._fake_password))

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
