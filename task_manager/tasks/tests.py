from task_manager.statuses.models import TaskStatus
from task_manager.labels.models import TaskLabel
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task
from task_manager.tasks.filters import TaskFilter

from django.test import TestCase
from task_manager.utils.test_crud import AbstractCRUDTest, LinkData


class TaskTest(AbstractCRUDTest, TestCase):
    def _init_test_data(self):
        self.links: LinkData = LinkData(
            list='tasks:list',
            create='tasks:create',
            create_redirect='tasks:list',
            update='tasks:update',
            update_redirect='tasks:list',
            delete='tasks:delete',
            delete_redirect='tasks:list',
            card='tasks:card',
        )
        self.form_fields: list = ['name',
                                  'description',
                                  'status',
                                  'executor',
                                  'labels']
        self.model = Task
        self.form = TaskForm
        self.has_filter = True
        self.filter_set_class = TaskFilter

    def _generate_data(self) -> dict:
        status: TaskStatus = TaskStatus(
            name=self.faker.text(max_nb_chars=100)
        )
        status.save()

        return {
            'name': self.faker.text(max_nb_chars=100),
            'description': self.faker.text(max_nb_chars=500),
            'status': self._get_status().id,
            'executor': self.user.id,
            'labels': self._get_label().id,
        }

    def test_self_task_filter(self):
        self._make_login()
        object_created_by_other_user = self._process_create()

        self._make_login()
        list_of_objects_data = self._process_create_list_of_objects()

        link_with_filter = self._get_link(self.links.list)

        response = self._get_request(link_with_filter,
                                     data={'self_tasks': 'on'})

        self.assertNotIn(str(object_created_by_other_user.obj.name),
                         response.rendered_content)

        for object_data in list_of_objects_data:
            self.assertIn(str(object_data.obj.name), response.rendered_content)

    def test_status_filter(self):
        self._make_login()
        list_of_objects_data = self._process_create_list_of_objects()

        link_with_filter = self._get_link(self.links.list)

        filtered_obj = list_of_objects_data[0].obj.status

        response = self._get_request(link_with_filter,
                                     data={'status': filtered_obj.id})

        self.assertIn(list_of_objects_data[0].obj.name,
                      response.rendered_content)

        for object_data in list_of_objects_data[1:]:
            self.assertNotIn(str(object_data.obj.name),
                             response.rendered_content)

    def test_executor_filter(self):
        self._make_login()
        first_obj = self._process_create()

        self._make_login()
        second_obj = self._process_create()

        link_with_filter = self._get_link(self.links.list)

        response = self._get_request(link_with_filter,
                                     data={
                                         'executor': first_obj.obj.executor.id
                                     })

        self.assertIn(first_obj.obj.name,
                      response.rendered_content)

        self.assertNotIn(second_obj.obj.name,
                         response.rendered_content)

    def test_labels_filter(self):
        self._make_login()
        first_obj = self._process_create()

        self._make_login()
        second_obj = self._process_create()

        link_with_filter = self._get_link(self.links.list)

        response = self._get_request(link_with_filter,
                                     data={'label': first_obj.data['labels']})

        self.assertIn(first_obj.obj.name,
                      response.rendered_content)

        self.assertNotIn(second_obj.obj.name,
                         response.rendered_content)

    def test_task_card(self):
        self._make_login()
        obj_data = self._process_create()
        obj = obj_data.obj

        data_link = self._get_link(self.links.card, pk=obj.id)
        response = self._get_request(data_link)

        desired_keys = [
            'name',
            'description',
            'status',
        ]
        for key in desired_keys:
            self.assertIn(
                str(getattr(obj, key)),
                response.rendered_content
            )

    def _get_status(self) -> TaskStatus:
        status: TaskStatus = TaskStatus(
            name=self.faker.text(max_nb_chars=100)
        )
        status.save()
        return status

    def _get_label(self):
        label: TaskLabel = TaskLabel(
            name=self.faker.text(max_nb_chars=100)
        )
        label.save()
        return label
