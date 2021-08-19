from nails_project.accounts.forms import SignUpForm
from tests.base.tests import NailsProjectTestCase


class TestSignUpForm(NailsProjectTestCase):

    def test_saveForm_whenValid_shouldBeValid(self):
        data = {
            'email': "testuser@mail.bg",
            'password1': 'stoychev123456',
            'password2': 'stoychev123456',

        }
        form = SignUpForm(data)
        self.assertTrue(form.is_valid())

    def test_saveForm_whenInvalid_shouldBeInvalid_emailError(self):
        data = {
            'email': "testusermail.bg",
            'password1': 'stoychev123456',
            'password2': 'stoychev123456',

        }
        form = SignUpForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('email'))

    def test_saveForm_whenInvalid_shouldBeInvalid_passwordError_toShort(self):
        data = {
            'email': "testuser@mail.bg",
            'password1': 'bobby',
            'password2': 'bobby',

        }
        form = SignUpForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('password2'))

    def test_saveForm_whenInvalid_shouldBeInvalid_passwordError_pass1AndPass2NotEqual(self):
        data = {
            'email': "testuser@mail.bg",
            'password1': 'bobby123456879',
            'password2': 'bobby254789654',

        }
        form = SignUpForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('password2'))