from task_manager.labels.forms import TaskLabelForm
from task_manager.labels.models import TaskLabel

from django.test import TestCase
from task_manager.utils.test_crud import AbstractCRUDTest, LinkData


class LabelsTest(AbstractCRUDTest, TestCase):
    def _init_test_data(self):
        self.links: LinkData = LinkData(
            list='labels:list',
            create='labels:create',
            create_redirect='labels:list',
            update='labels:update',
            update_redirect='labels:list',
            delete='labels:delete',
            delete_redirect='labels:list',
        )
        self.form_fields: list = ['name']
        self.model = TaskLabel
        self.form = TaskLabelForm

    def _generate_data(self) -> dict:
        return {
            'name': self.faker.text(max_nb_chars=100),
        }
