from collections import OrderedDict

from django.template.response import TemplateResponse
from django.test import TestCase, Client
from django.urls import reverse_lazy

from django.contrib.auth import get_user_model

from faker import Faker
from faker.generator import Generator

from task_manager.statuses.models import TaskStatus
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task


class CRUDTaskTest(TestCase):
    """Test user registration."""

    def setUp(self):
        """Create a test database."""
        self.client: Client = Client()
        self.faker: Generator = Faker()
        self._make_login()
        self._init_status()

    def _init_status(self):
        self._status: TaskStatus = TaskStatus(
            name=self.faker.text(max_nb_chars=100)
        )
        self._status.save()

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
            reverse_lazy('tasks:create'),
        )
        form_fields: OrderedDict = TaskForm.base_fields
        self._assert_field('name', form_fields, response)
        self._assert_field('description', form_fields, response)
        self._assert_field('status', form_fields, response)
        self._assert_field('executor', form_fields, response)

    def _assert_field(self,
                      field: str,
                      form_fields: OrderedDict,
                      response: TemplateResponse):
        self.assertIn(
            str(form_fields[field].label),
            response.rendered_content,
        )
        self.assertIn(
            str(form_fields[field].help_text),
            response.rendered_content,
        )

    def test_success_create_task(self):
        response = self._create_task()
        self.assertRedirects(response, reverse_lazy('tasks:list'))
        self.assertTrue(self._get_task_object())

    def test_success_update_task(self):
        self._create_task()
        task_obj: Task = self._get_task_object()
        new_name: str = self.faker.text(max_nb_chars=100)
        new_description: str = self.faker.text(max_nb_chars=500)
        response: TemplateResponse = self.client.post(
            reverse_lazy('tasks:update', kwargs={'pk': task_obj.id}),
            data={
                'name': new_name,
                'description': new_description,
                'status': self._status.id,
                'executor': self._user_id
            }
        )
        self.assertRedirects(response, reverse_lazy('tasks:list'))
        self.assertTrue(
            Task.objects.filter(pk=task_obj.id,
                                name=new_name,
                                description=new_description),
        )
        self.assertFalse(
            Task.objects.filter(pk=task_obj.id,
                                name=self._name,
                                description=self._description),
        )

    def test_success_delete_task(self):
        self._create_task()
        task_obj: Task = self._get_task_object()
        response: TemplateResponse = self.client.post(
            reverse_lazy('tasks:delete', kwargs={'pk': task_obj.id}),
        )
        self.assertRedirects(response, reverse_lazy('tasks:list'))
        self.assertFalse(self._get_task_object())

    def _create_task(self):
        self._name: str = self.faker.text(max_nb_chars=100)
        self._description: str = self.faker.text(max_nb_chars=500)
        user = get_user_model().objects.filter(username=self._user_name).first()
        self._user_id: int = user.id
        response: TemplateResponse = self.client.post(
            reverse_lazy('tasks:create'),
            data={
                'name': self._name,
                'description': self._description,
                'status': self._status.id,
                'executor': self._user_id
            }
        )
        return response

    def _get_task_object(self) -> Task:
        return Task.objects.filter(name=self._name,
                                   description=self._description,
                                   status=self._status.id,
                                   executor=self._user_id).first()
