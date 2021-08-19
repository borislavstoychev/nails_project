from tests.base.mixins import UserTestUtils, ScheduleTestUtils
from tests.base.tests import NailsProjectTestCase
from django.urls import reverse


class ScheduleCreateStaffOnlyTests(NailsProjectTestCase, UserTestUtils, ScheduleTestUtils):

    def test_schedule_withNoSchedule(self):
        nails_user = self.create_user(email='nails@user.com', password='12345qwe', is_active=True, is_staff=True)
        self.client.force_login(nails_user)
        response = self.client.get(reverse('schedule create'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(0, len(list(response.context['schedules'])))
        self.assertTemplateUsed('schedule/schedule.html')

    def test_schedule_withSchedule_shouldReturnListSchedule(self):
        nails_user = self.create_user(email='nails@user.com', password='12345qwe', is_active=True, is_staff=True)
        self.client.force_login(nails_user)
        schedule = self.create_schedule(
            date='2021-10-12',
            start_time='09:30',
            end_time='22:30',
        )
        response = self.client.get(reverse('schedule create'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(list(response.context['schedules'])))
        self.assertTemplateUsed('schedule/schedule.html')

    def test_scheduleCreate_shouldCreateSchedule(self):
        nails_user = self.create_user(email='nails@user.com', password='12345qwe', is_active=True, is_staff=True)
        self.client.force_login(nails_user)
        response = self.client.post(reverse('schedule create'), data={
            'date': '2021-10-12',
            'start_time': '09:30',
            'end_time': '22:30',
        })
        self.assertEqual(302, response.status_code)
        self.assertTemplateUsed('schedule/schedule.html')
        response_get = self.client.get(reverse('schedule create'))
        self.assertEqual(1, len(list(response_get.context['schedules'])))
        self.assertTemplateUsed('schedule/schedule.html')

    def test_scheduleCreate_whenUserNotStaff_shouldBeForbidden(self):
        nails_user = self.create_user(email='nails@user.com', password='12345qwe', is_active=True)
        self.client.force_login(nails_user)
        response = self.client.post(reverse('schedule create'), data={
            'date': '2021-10-12',
            'start_time': '09:30',
            'end_time': '22:30',
        })
        self.assertEqual(403, response.status_code)
        self.assertTemplateUsed('schedule/schedule.html')
        response_get = self.client.get(reverse('schedule create'))
        self.assertEqual(403, response_get.status_code)
        self.assertTemplateUsed('schedule/schedule.html')
