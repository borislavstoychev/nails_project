from tests.base.mixins import UserTestUtils, NailsTestUtils
from tests.base.tests import NailsProjectTestCase
from django.urls import reverse


class SingOutViewTest(NailsTestUtils, UserTestUtils,NailsProjectTestCase):
    def test_singOut_shouldGetSignInPage(self):
        self.client.force_login(self.user)
        log_out = self.client.get(reverse('sign out user'))
        self.assertEqual(302, log_out.status_code)
