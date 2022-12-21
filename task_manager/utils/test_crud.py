from abc import ABC, abstractmethod
from pydantic import BaseModel

from django.test import Client
from django.urls import reverse_lazy
from django.db.models import Model
from collections import OrderedDict

from typing import Type

from django.contrib.auth.models import User

from django.template.response import TemplateResponse

from faker import Faker


class LinkData(BaseModel):
    list: str
    create: str
    create_redirect: str
    update: str
    update_redirect: str
    delete: str
    delete_redirect: str


class AbstractCRUDTest(ABC):
    def setUp(self) -> None:
        self.client: Client = Client()
        self.faker: Faker = Faker()
        self._init_test_data()
        self.filter_keys: list = self._get_filter_keys()

    @property
    def user(self):
        return self._user

    @abstractmethod
    def _init_test_data(self):
        self.links: LinkData = None
        self.form_fields: list = None
        self.model = None
        self.form = None

    @abstractmethod
    def _generate_data(self) -> dict:
        pass

    def _generate_update_data(self) -> dict:
        return self._generate_data()

    def _get_filter_keys(self) -> list:
        return self.form_fields

    def test_form(self, need_login: bool = True):
        if need_login:
            self._make_login()
        response: TemplateResponse = self.client.get(
            reverse_lazy(self.links.create),
        )
        form_fields: OrderedDict = self.form.base_fields
        for field in self.form_fields:
            self._assert_field(field,
                               form_fields,
                               response)

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

    def _make_login(self):
        self._user: User = self._generate_user()
        self.client.login(username=self._user_name,
                          password=self._fake_password)

    def _generate_user(self) -> User:
        self._fake_password: str = self.faker.password(length=10)
        self._user_name: str = self.faker.user_name()
        user: User = User(username=self._user_name)
        user.set_password(self._fake_password)
        user.save()
        return user

    def test_create(self, need_login: bool = True):
        response, data, obj_id = self._process_create(need_login)
        self.assertRedirects(response,
                             reverse_lazy(self.links.create_redirect))
        self.assertTrue(self._get_object(**data))

    def _process_create(self,
                        need_login: bool = True
                        ) -> tuple[TemplateResponse, dict, int]:
        if need_login:
            self._make_login()
        data: dict = self._generate_data()
        path: str = reverse_lazy(self.links.create)
        response: TemplateResponse = self._post_request(path, data)

        obj: Type[Model] = self._get_object(**data)
        obj_id: int = obj.id

        return response, data, obj_id

    def test_update(self, need_login: bool = True):
        create_response, data, obj_id = self._process_create(need_login)

        if need_login:
            self._make_login()

        update_path: str = reverse_lazy(
            self.links.update,
            kwargs={'pk': obj_id}
        )
        new_data: dict = self._generate_update_data()
        update_response = self._post_request(update_path, new_data)

        self.assertRedirects(update_response,
                             reverse_lazy(self.links.update_redirect))
        self.assertTrue(self._get_object(**new_data, pk=obj_id))
        self.assertFalse(self._get_object(**data))

    def test_delete(self, need_login: bool = True):
        create_response, data, obj_id = self._process_create(need_login)

        if need_login:
            self._make_login()

        delete_path: str = reverse_lazy(
            self.links.delete,
            kwargs={'pk': obj_id}
        )
        delete_response = self._post_request(delete_path)

        self.assertRedirects(delete_response,
                             reverse_lazy(self.links.delete_redirect))
        self.assertFalse(self._get_object(**data))
        self.assertFalse(self._get_object(pk=obj_id))

    def _post_request(self, path: str, data: dict = None) -> TemplateResponse:
        response: TemplateResponse = self.client.post(
            path,
            data=data
        )
        return response

    def _get_object(self, **kwargs) -> Type[Model]:
        _filter: dict = {
            key: kwargs[key]
            for key in kwargs.keys()
            if key in self.filter_keys or key == 'pk'
        }
        self._object = self.model.objects.filter(**_filter).first()
        return self._object
