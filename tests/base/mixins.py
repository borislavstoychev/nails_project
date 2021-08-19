from django.contrib.auth import get_user_model

from nails_project.schedule.models import Schedule
from nails_project.nails.models import Feedback, Like

UserModel = get_user_model()


class NailsTestUtils:

    def create_feedback(self, **kwargs):
        return Feedback.objects.create(**kwargs)


    def create_feedback_with_like(self, like_user, **kwargs):
        feedback = self.create_feedback(**kwargs)
        Like.objects.create(
            feedback=feedback,
            user=like_user,
        )
        return feedback


class ScheduleTestUtils:

    def create_schedule(self, **kwargs):
        return Schedule.objects.create(**kwargs)


class UserTestUtils:
    def create_user(self, **kwargs):
        return UserModel.objects.create_user(**kwargs)

    def create_superuser(self, **kwargs):
        return UserModel.objects.create_superuser