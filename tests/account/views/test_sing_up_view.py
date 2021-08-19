from tests.base.mixins import UserTestUtils, NailsTestUtils
from tests.base.tests import NailsProjectTestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class SignUpPageTests(NailsProjectTestCase, UserTestUtils, NailsTestUtils):
    def setUp(self) -> None:
        self.email = 'testuser@email.com'
        self.password = 'boreto95478'

    def test_signupPage_viewName_andTemplate(self):
        response = self.client.get(reverse('sign up user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='account/auth/sign_up.html')

    def test_signup_formWhenUser_notExist(self):
        response = self.client.post(reverse('sign up user'), data={
            'email': self.email,
            'password1': self.password,
            'password2': self.password
        })
        self.assertEqual(response.status_code, 200)

        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)

    def test_signup_formWhenUser_Exist_shouldNotCreate(self):
        user = self.create_user(email=self.email, password='testuser1234')
        response = self.client.post(reverse('sign up user'), data={
            'email': self.email,
            'password1': self.password,
            'password2': self.password
        })
        self.assertEqual(response.status_code, 200)

        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)
