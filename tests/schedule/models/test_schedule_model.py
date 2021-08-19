from django.core.exceptions import ValidationError

from nails_project.schedule.models import Schedule
from tests.base.tests import NailsProjectTestCase


class ScheduleModelTests(NailsProjectTestCase):

    def test_saveModel_whenValid_shouldBeValid(self):
        data = {
            'date': "2021-08-10",
            'start_time': '09:00',
            'end_time': '19:00',
        }
        obj = Schedule(**data)
        obj.full_clean()
        obj.save()
        self.assertEqual('2021-08-10', obj.date.strftime('%Y-%m-%d'))
        self.assertEqual('09:00', obj.start_time.strftime('%H:%M'))
        self.assertEqual('19:00', obj.end_time.strftime('%H:%M'))
        self.assertTrue(Schedule.objects.filter(pk=obj.id).exists())

    def test_saveModel_whenInvalid_shouldBeInvalid_dateError(self):
        data = {
            'date': None,
            'start_time': '09:00',
            'end_time': '19:00',
        }
        with self.assertRaises(ValidationError) as error:
            obj = Schedule(**data)
            obj.full_clean()
            obj.save()
        self.assertIsNotNone(error)
        self.assertFalse(Schedule.objects.all().exists())

    def test_saveModel_whenValid_shouldBeValid_startTimeNone(self):
        data = {
            'date': '2021-08-10',
            'start_time': None,
            'end_time': '19:00',
        }
        obj = Schedule(**data)
        obj.full_clean()
        obj.save()
        self.assertEqual('2021-08-10', obj.date.strftime('%Y-%m-%d'))
        self.assertIsNone(obj.start_time)
        self.assertEqual('19:00', obj.end_time.strftime('%H:%M'))
        self.assertTrue(Schedule.objects.filter(pk=obj.id).exists())

    def test_saveModel_whenValid_shouldBeValid_endTimeNone(self):
        data = {
            'date': '2021-08-10',
            'start_time': '19:00',
            'end_time': None,
        }
        obj = Schedule(**data)
        obj.full_clean()
        obj.save()
        self.assertEqual('2021-08-10', obj.date.strftime('%Y-%m-%d'))
        self.assertIsNone(obj.end_time)
        self.assertEqual('19:00', obj.start_time.strftime('%H:%M'))
        self.assertTrue(Schedule.objects.filter(pk=obj.id).exists())