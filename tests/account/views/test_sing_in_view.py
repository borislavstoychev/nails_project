from tests.base.mixins import UserTestUtils, NailsTestUtils
from tests.base.tests import NailsProjectTestCase
from django.urls import reverse


class SingInViewTest(NailsTestUtils, UserTestUtils,NailsProjectTestCase):

    def test_singInVieName_and_templateName(self):
        response = self.client.get(reverse('sign in user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='account/auth/sign_in.html')

    def test_singIn_whenUserIsActive_shouldGetHomePageWithUser(self):
        nails_user = self.create_user(email='nails@user.com', password='12345qwe', is_active=True)
        response = self.client.post(reverse('sign in user'), data={
            "username": 'nails@user.com',
            'password': '12345qwe'
        }, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_singIn_whenUserIsNotActive_shouldStayOnSingIn(self):
        nails_user = self.create_user(email='nails@user.com', password='12345qwe')
        response = self.client.post(reverse('sign in user'), data={
            "username": 'nails@user.com',
            'password': '12345qwe'
        }, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertNotEqual(self.user.id, response.context['user'].is_authenticated)
