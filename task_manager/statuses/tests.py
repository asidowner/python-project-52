from task_manager.statuses.forms import TaskStatusForm
from task_manager.statuses.models import TaskStatus

from django.test import TestCase
from task_manager.utils.test_crud import AbstractCRUDTest, LinkData


class StatusTest(AbstractCRUDTest, TestCase):
    def _init_test_data(self):
        self.links: LinkData = LinkData(
            list='statuses:list',
            create='statuses:create',
            create_redirect='statuses:list',
            update='statuses:update',
            update_redirect='statuses:list',
            delete='statuses:delete',
            delete_redirect='statuses:list',
        )
        self.form_fields: list = ['name']
        self.model = TaskStatus
        self.form = TaskStatusForm

    def _generate_data(self) -> dict:
        return {
            'name': self.faker.text(max_nb_chars=100),
        }
