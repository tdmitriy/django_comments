from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.signals import pre_social_login
from allauth.account.signals import user_signed_up
from allauth.account.utils import perform_login
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.shortcuts import redirect
from django.conf import settings
from .models import UserProfile
import hashlib


# django allauth facebook redirects to signup when retrieved email matches an existing user's email
# see here http://stackoverflow.com/a/24358708/5433344
class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Overrides allauth.socialaccount.adapter.DefaultSocialAccountAdapter.pre_social_login to
    perform some actions right after successful login
    """

    def pre_social_login(self, request, sociallogin):
        pass  # TODO Future: To perform some actions right after successful login


@receiver(pre_social_login)
def link_to_local_user(sender, request, sociallogin, **kwargs):
    """ Login and redirect
    This is done in order to tackle the situation where user's email retrieved
    from one provider is different from already existing email in the database
    (e.g facebook and google both use same email-id). Specifically, this is done to
    tackle following issues:
    * https://github.com/pennersr/django-allauth/issues/215

    """

    email_address = sociallogin.account.extra_data['email']
    existing_user = User.objects.filter(email=email_address).first()
    link_social_info_to_superuser(existing_user, sociallogin)
    if existing_user:
        perform_login(request, existing_user, email_verification='optional')
        raise ImmediateHttpResponse(redirect(settings.LOGIN_REDIRECT_URL))


# For example we can create superuser via console and UserProfile for him will be empty, so fill it
def link_social_info_to_superuser(user, sociallogin):
    if user and user.is_superuser:
        user_profile = UserProfile.objects.filter(user=user).first()
        if not user_profile:
            user.first_name = sociallogin.account.extra_data['first_name']
            user.last_name = sociallogin.account.extra_data['last_name']
            user.email = sociallogin.account.extra_data['email']
            user.save()

            picture_url = get_user_avatar_url(user, sociallogin)
            profile = UserProfile(user=user, avatar_url=picture_url)
            profile.save()


# create user profile after facebook signed up
@receiver(user_signed_up)
def on_signed_up(request, user, sociallogin=None, **kwargs):
    picture_url = get_user_avatar_url(user, sociallogin)
    profile = UserProfile(user=user, avatar_url=picture_url)
    profile.save()


def get_user_avatar_url(user, sociallogin):
    picture_size = 40
    default_img_url = "http://www.gravatar.com/avatar/{0}?s={1}"

    avatar_url = default_img_url.format(
        hashlib.md5(user.email.lower().encode('UTF-8')).hexdigest(),
        picture_size
    )

    if sociallogin and sociallogin.account.provider == 'facebook':
        formatted_rl = "http://graph.facebook.com/{0}/picture?width={1}&height={1}"
        avatar_url = formatted_rl.format(sociallogin.account.uid, picture_size)

    return avatar_url
