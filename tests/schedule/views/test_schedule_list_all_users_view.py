from tests.base.mixins import UserTestUtils, ScheduleTestUtils
from tests.base.tests import NailsProjectTestCase
from django.urls import reverse


class ScheduleListViewTests(NailsProjectTestCase, UserTestUtils, ScheduleTestUtils):

    def test_schedule_withUser_whenNoSchedule(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('schedule view'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(0, len(list(response.context['monday'])))
        self.assertEqual(0, len(list(response.context['tuesday'])))
        self.assertEqual(0, len(list(response.context['wednesday'])))
        self.assertEqual(0, len(list(response.context['thursday'])))
        self.assertEqual(0, len(list(response.context['friday'])))
        self.assertEqual(0, len(list(response.context['saturday'])))
        self.assertEqual(0, len(list(response.context['sunday'])))
        self.assertTemplateUsed('schedule/schedule_view.html')

    def test_schedule_withoutUser_whenNoSchedule(self):
        response = self.client.get(reverse('schedule view'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(0, len(list(response.context['monday'])))
        self.assertEqual(0, len(list(response.context['tuesday'])))
        self.assertEqual(0, len(list(response.context['wednesday'])))
        self.assertEqual(0, len(list(response.context['thursday'])))
        self.assertEqual(0, len(list(response.context['friday'])))
        self.assertEqual(0, len(list(response.context['saturday'])))
        self.assertEqual(0, len(list(response.context['sunday'])))
        self.assertTemplateUsed('schedule/schedule_view.html')

    def test_schedule_withUser_whenScheduleOnSaturday(self):
        self.client.force_login(self.user)
        schedule = self.create_schedule(
            date='2021-08-07',
            start_time='09:30',
            end_time='22:30',
        )
        response = self.client.get(reverse('schedule view'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(0, len(list(response.context['monday'])))
        self.assertEqual(0, len(list(response.context['tuesday'])))
        self.assertEqual(0, len(list(response.context['wednesday'])))
        self.assertEqual(0, len(list(response.context['thursday'])))
        self.assertEqual(0, len(list(response.context['friday'])))
        self.assertEqual(1, len(list(response.context['saturday'])))
        self.assertEqual(0, len(list(response.context['sunday'])))
        self.assertTemplateUsed('schedule/schedule_view.html')

    def test_schedule_withoutUser_whenScheduleOnSaturday(self):
        schedule = self.create_schedule(
            date='2021-08-07',
            start_time='09:30',
            end_time='22:30',
        )
        response = self.client.get(reverse('schedule view'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(0, len(list(response.context['monday'])))
        self.assertEqual(0, len(list(response.context['tuesday'])))
        self.assertEqual(0, len(list(response.context['wednesday'])))
        self.assertEqual(0, len(list(response.context['thursday'])))
        self.assertEqual(0, len(list(response.context['friday'])))
        self.assertEqual(1, len(list(response.context['saturday'])))
        self.assertEqual(0, len(list(response.context['sunday'])))
        self.assertTemplateUsed('schedule/schedule_view.html')