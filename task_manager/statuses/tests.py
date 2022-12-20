from collections import OrderedDict

from django.template.response import TemplateResponse
from django.test import TestCase, Client
from django.urls import reverse_lazy
from faker import Faker
from faker.generator import Generator

from task_manager.statuses.forms import TaskStatusForm
from task_manager.statuses.models import TaskStatus


class CRUDStatusTest(TestCase):
    """Test user registration."""

    def setUp(self):
        """Create a test database."""
        self.client: Client = Client()
        self.faker: Generator = Faker()
        self._make_login()

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

    def test_form(self):
        response: TemplateResponse = self.client.get(
            reverse_lazy('statuses:list'),
        )
        form_fields: OrderedDict = TaskStatusForm.base_fields
        self._assert_name(form_fields, response)

    def _assert_name(self,
                     form_fields: OrderedDict,
                     response: TemplateResponse):
        self.assertIn(
            str(form_fields['name'].label),
            response.rendered_content,
        )
        self.assertIn(
            str(form_fields['name'].help_text),
            response.rendered_content,
        )

    def test_success_create_status(self):
        response: TemplateResponse = self._create_status()
        self.assertRedirects(response, reverse_lazy('statuses:list'))
        self.assertTrue(
            TaskStatus.objects.filter(name=self._status_name),
        )

    def test_success_update_status(self):
        self._create_status()
        status_obj: TaskStatus = self._get_status_object()
        new_status_name = self.faker.text(max_nb_chars=100)
        response: TemplateResponse = self.client.post(
            reverse_lazy('statuses:update', kwargs={'pk': status_obj.id}),
            data={
                'name': new_status_name
            }
        )
        self.assertRedirects(response, reverse_lazy('statuses:list'))
        self.assertTrue(
            TaskStatus.objects.filter(pk=status_obj.id, name=new_status_name),
        )
        self.assertFalse(
            TaskStatus.objects.filter(pk=status_obj.id, name=self._status_name),
        )

    def test_success_delete_status(self):
        self._create_status()
        status_obj: TaskStatus = self._get_status_object()
        response: TemplateResponse = self.client.post(
            reverse_lazy('statuses:delete', kwargs={'pk': status_obj.id}),
        )
        self.assertRedirects(response, reverse_lazy('statuses:list'))
        self.assertFalse(
            TaskStatus.objects.filter(pk=status_obj.id),
        )

    def _create_status(self) -> TemplateResponse:
        self._status_name: str = self.faker.text(max_nb_chars=100)
        response: TemplateResponse = self.client.post(
            reverse_lazy('statuses:create'),
            data={
                'name': self._status_name
            }
        )
        return response

    def _get_status_object(self) -> TaskStatus:
        return TaskStatus.objects.filter(name=self._status_name).first()
