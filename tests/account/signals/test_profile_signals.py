from unittest.mock import patch
from nails_project.accounts.forms import SignUpForm
from tests.base.tests import NailsProjectTestCase


class SignalsProfile(NailsProjectTestCase):

    @patch('django.db.models.signals.ModelSignal.send')
    def test_profileCreate_signal(self, mock):
        data = {
            'email': "testuser@mail.bg",
            'password1': 'stoychev123456',
            'password2': 'stoychev123456',

        }
        form = SignUpForm(data)
        form.save()

        # Check that your signal was called.
        self.assertTrue(mock.called)
        self.assertEqual(4, mock.call_count)


