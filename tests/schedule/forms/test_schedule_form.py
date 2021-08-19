from nails_project.schedule.forms import ScheduleForm
from tests.base.tests import NailsProjectTestCase


class TestScheduleCreateForm(NailsProjectTestCase):

    def test_saveForm_whenValid_shouldBeValid(self):
        data = {
            'date': "2021-08-10",
            'start_time': '09:00',
            'end_time': '19:00',
        }
        form = ScheduleForm(data)
        self.assertTrue(form.is_valid())

    def test_saveForm_whenInValid_shouldBeInValid_dateError(self):
        data = {
            'date': None,
            'start_time': '09:00',
            'end_time': '19:00',
        }
        form = ScheduleForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error(field='date'))