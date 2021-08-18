from django.template import Library

from nails_project.accounts.models import Profile

register = Library()


@register.inclusion_tag('common/complete_tag.html', takes_context=True)
def profile_complete_notification(context):
    user_id = context.request.user.id
    profile = Profile.objects.get(pk=user_id)
    return {
        'is_complete': profile.is_complete,
        'user_id': user_id

    }