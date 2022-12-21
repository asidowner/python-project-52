from task_manager.statuses.models import TaskStatus
from task_manager.labels.models import TaskLabel
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task

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
        )
        self.form_fields: list = ['name',
                                  'description',
                                  'status',
                                  'executor',
                                  'labels']
        self.model = Task
        self.form = TaskForm
        self._status: TaskStatus = TaskStatus(
            name=self.faker.text(max_nb_chars=100)
        )
        self._status.save()

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

    def _generate_data(self) -> dict:
        return {
            'name': self.faker.text(max_nb_chars=100),
            'description': self.faker.text(max_nb_chars=500),
            'status': self._get_status().id,
            'executor': self.user.id,
            'labels': self._get_label().id,
        }
