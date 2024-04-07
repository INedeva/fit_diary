from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserRegistrationTestCase(TestCase):

    def test_post_user_register__stay_logged_in__expect_302_and_correct_template(self):
        USER_DATA = {
            'email': 'testuser@abv.bg',
            'password1': '01234578Aa_',
            'password2': '01234578Aa_',
        }

        response = self.client.post(reverse('register-user'), USER_DATA)

        self.assertRedirects(response, reverse('diary'))

        user = UserModel.objects.get(email='testuser@abv.bg')
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)

        self.assertTrue(self.client.login(email='testuser@abv.bg', password='01234578Aa_'))
