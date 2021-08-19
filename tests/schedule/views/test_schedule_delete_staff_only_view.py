from nails_project.schedule.models import Schedule
from tests.base.mixins import UserTestUtils, ScheduleTestUtils
from tests.base.tests import NailsProjectTestCase
from django.urls import reverse


class ScheduleDeleteStaffOnlyTests(NailsProjectTestCase, UserTestUtils, ScheduleTestUtils):

    def test_schedule_delete_withNoSchedule(self):
        nails_user = self.create_user(email='nails@user.com', password='12345qwe', is_active=True, is_staff=True)
        self.client.force_login(nails_user)
        response = self.client.get(reverse('delete schedule', kwargs={'pk': 1}))
        self.assertEqual(404, response.status_code)
        self.assertTemplateUsed('schedule/schedule.html')

    def test_scheduleDelete_withSchedule_shouldReturnListSchedule(self):
        nails_user = self.create_user(email='nails@user.com', password='12345qwe', is_active=True, is_staff=True)
        self.client.force_login(nails_user)
        schedule = self.create_schedule(
            date='2021-10-12',
            start_time='09:30',
            end_time='22:30',
        )
        response = self.client.post(reverse('delete schedule', kwargs={"pk": schedule.id}))
        self.assertEqual(302, response.status_code)
        self.assertTemplateUsed('schedule/schedule.html')
        existing_schedule = Schedule.objects.filter(pk=schedule.id).exists()
        self.assertFalse(existing_schedule)
        response_get = self.client.get(reverse('schedule create'))
        self.assertEqual(0, len(list(response_get.context['schedules'])))
        self.assertTemplateUsed('schedule/schedule.html')

    def test_scheduleDelete_whenUserNotStaff_shouldBeForbidden(self):
        self.client.force_login(self.user)
        schedule = self.create_schedule(
            date='2021-10-12',
            start_time='09:30',
            end_time='22:30',
        )
        response = self.client.post(reverse('delete schedule', kwargs={"pk": schedule.id}))
        self.assertEqual(403, response.status_code)
        self.assertTemplateUsed('schedule/schedule.html')
        existing_schedule = Schedule.objects.filter(pk=schedule.id).exists()
        self.assertTrue(existing_schedule)

