from nails_project.accounts.forms import SignInForm
from tests.base.mixins import UserTestUtils, NailsTestUtils
from tests.base.tests import NailsProjectTestCase


class TestSignInForm(NailsTestUtils, UserTestUtils, NailsProjectTestCase):

    def test_saveForm_whenValid_shouldBeValid(self):
        nails_user = self.create_user(email='nails@user.com', password='12345qwe', is_active=True)
        data = {
            "username": 'nails@user.com',
            'password': '12345qwe'

        }
        form = SignInForm(data)
        self.assertFalse(form.has_error('username'))
        self.assertFalse(form.has_error('password'))


