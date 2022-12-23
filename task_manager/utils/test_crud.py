from abc import ABC, abstractmethod
from pydantic import BaseModel

from django.test import Client
from django.urls import reverse_lazy
from django.db.models import Model, QuerySet
from django.forms import Form
from collections import OrderedDict

from django.contrib.auth.models import User

from django_filters import FilterSet
from django.http import HttpResponseBase
from django.template.response import TemplateResponse

from faker import Faker

_NUMBER_OF_ITEMS_TO_CREATE: int = 3


class LinkData(BaseModel):
    list: str
    create: str
    create_redirect: str
    update: str
    update_redirect: str
    delete: str
    delete_redirect: str
    card: str = None


class CreateProcessResult(BaseModel):
    response: HttpResponseBase
    data: dict
    obj: Model

    class Config:
        arbitrary_types_allowed = True


def skip_if_false(flag):
    def deco(f):
        def wrapper(self, *args, **kwargs):
            if not getattr(self, flag):
                reason = f'Skip because {flag=} is False'
                self.skipTest(reason)
            else:
                f(self, *args, **kwargs)

        return wrapper

    return deco


class AbstractCRUDTest(ABC):
    has_filter = False

    def setUp(self) -> None:
        self.client: Client = Client()
        self.faker: Faker = Faker()
        self._init_test_data()
        self.filter_object_keys: list = self._get_filter_object_keys()

    @property
    def user(self):
        return self._user

    @abstractmethod
    def _init_test_data(self):
        """
        * self.links Type[LinkData] - DataClass with links. required
        * self.model Type[Model] - Main db model of tested crud required
        * self.form Type[Form] - Main form of tested crud. required
        * self.form_fields Type[list] - list of create form fields
        * self.has_filter Type[bool] - An indication of the need to test the filtering of the list
        * self.has_filter Type[bool] - An indication of the need to test the filtering of the list
        * self.filter_set_class Type[FilterSet] - class of FilterSet
        """  # noqa: E501
        self.links: LinkData = None
        self.model: Model = None
        self.form: Form = None
        self.form_fields: list = None
        self.has_filter: bool = False
        self.filter_set_class: FilterSet = None

    @abstractmethod
    def _generate_data(self) -> dict:
        pass

    def _generate_update_data(self) -> dict:
        return self._generate_data()

    def _get_filter_object_keys(self) -> list:
        return self.form_fields

    def test_form(self, need_login: bool = True):
        if need_login:
            self._make_login()

        response = self._get_request(self._get_link(self.links.create))
        form_fields: OrderedDict = self.form.base_fields

        for field in self.form_fields:
            self._assert_field(field,
                               form_fields,
                               response)

    @staticmethod
    def _get_link(path: str, **kwargs) -> str:
        return reverse_lazy(path, kwargs=kwargs)

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
        if need_login:
            self._make_login()
        create_process_result = self._process_create()
        self.assertRedirects(create_process_result.response,
                             reverse_lazy(self.links.create_redirect))
        self.assertTrue(
            self._get_object_with_filter_fields(**create_process_result.data)
        )

    def _process_create(self) -> CreateProcessResult:
        data: dict = self._generate_data()
        path: str = reverse_lazy(self.links.create)
        response: TemplateResponse = self._post_request(path, data)

        obj: Model = self._get_object_with_filter_fields(**data)
        self.assertTrue(obj)

        return CreateProcessResult(response=response, data=data, obj=obj)

    def test_read(self, need_login: bool = True):
        if need_login:
            self._make_login()

        created_list_ob_objects = self._process_create_list_of_objects()
        response = self._get_request(self._get_link(self.links.list))

        for item in created_list_ob_objects:
            self.assertIn(str(item.obj), response.rendered_content)

    def _process_create_list_of_objects(self,
                                        count=_NUMBER_OF_ITEMS_TO_CREATE
                                        ) -> list[CreateProcessResult]:
        list_of_objects: list[CreateProcessResult] = []

        for create_process_result in range(0, count):
            list_of_objects.append(self._process_create())
        return list_of_objects

    @skip_if_false('has_filter')
    def test_exists_filter_keys(self, need_login: bool = True):
        if need_login:
            self._make_login()

        response = self._get_request(self._get_link(self.links.list))
        filter_keys = self.filter_set_class.get_filters().keys()
        for key in filter_keys:
            self.assertIn(str(key), response.rendered_content)

    def test_update(self, need_login: bool = True):
        if need_login:
            self._make_login()

        create_process_result = self._process_create()

        obj_id: int = create_process_result.obj.id

        update_path: str = reverse_lazy(
            self.links.update,
            kwargs={'pk': obj_id}
        )
        new_data: dict = self._generate_update_data()
        update_response = self._post_request(update_path, new_data)

        self.assertRedirects(update_response,
                             reverse_lazy(self.links.update_redirect))
        self.assertTrue(
            self._get_object_with_filter_fields(**new_data, pk=obj_id)
        )
        self.assertFalse(
            self._get_object_with_filter_fields(**create_process_result.data)
        )

    def test_delete(self, need_login: bool = True):
        if need_login:
            self._make_login()

        create_process_result = self._process_create()

        obj_id: int = create_process_result.obj.id

        delete_path: str = reverse_lazy(
            self.links.delete,
            kwargs={'pk': obj_id}
        )
        delete_response = self._post_request(delete_path)

        self.assertRedirects(delete_response,
                             reverse_lazy(self.links.delete_redirect))
        self.assertFalse(
            self._get_object_with_filter_fields(**create_process_result.data)
        )
        self.assertFalse(
            self._get_object_with_filter_fields(pk=obj_id)
        )

    def _get_request(self, path: str, data: dict = None) -> TemplateResponse:
        response: TemplateResponse = self.client.get(
            path,
            data=data
        )
        return response

    def _post_request(self, path: str, data: dict = None) -> TemplateResponse:
        response: TemplateResponse = self.client.post(
            path,
            data=data
        )
        return response

    def _get_object_with_filter_fields(self, **kwargs) -> Model:
        _filtered_keys: dict = {
            key: kwargs[key]
            for key in kwargs.keys()
            if key in self.filter_object_keys or key == 'pk'
        }
        return self._get_object(**_filtered_keys)

    def _get_object(self, **kwargs) -> Model:
        self._object = self._get_all_objects(**kwargs).first()
        return self._object

    def _get_all_objects(self, **kwargs) -> QuerySet:
        return self.model.objects.filter(**kwargs)
