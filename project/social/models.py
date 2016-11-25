import hashlib

from allauth.socialaccount.models import SocialAccount
from django.db import models
from django.contrib.auth.models import User
from allauth.account.signals import user_signed_up
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, related_name='profile')
    avatar_url = models.CharField(max_length=256, blank=True, null=True)

    def full_name(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

    class Meta:
        db_table = "user_profile"

    def __str__(self):
        return "UserProfile[%d, %s]" % (self.id, self.full_name())


class Comment(models.Model):
    user = models.ForeignKey(UserProfile, null=False)
    content = models.TextField(null=False)
    pub_date = models.DateTimeField(null=False, auto_now_add=True)

    class Meta:
        db_table = 'comments'
        ordering = ['-pub_date']

    def __str__(self):
        return "Comment[%d, %s, %s]" % (self.id, self.content, self.pub_date)


class Reply(models.Model):
    user = models.ForeignKey(UserProfile, null=False)
    comment = models.ForeignKey(Comment, null=False)
    parent = models.ForeignKey('self', null=True, blank=True)
    content = models.TextField(null=False)
    pub_date = models.DateTimeField(null=False, auto_now_add=True)

    class Meta:
        db_table = 'replies'
        ordering = ['parent_id', 'pub_date']

    def __str__(self):
        return "Reply[%s, %s]" % (self.content, self.pub_date)


@receiver(user_signed_up)
def on_signed_up(request, user, sociallogin=None, **kwargs):
    picture_size = 40

    picture_url = "http://www.gravatar.com/avatar/{0}?s={1}".format(
        hashlib.md5(user.email.encode('UTF-8')).hexdigest(),
        picture_size
    )

    if sociallogin:
        if sociallogin.account.provider == 'facebook':
            fb_uid = SocialAccount.objects.filter(user_id=user.id, provider='facebook')
            img_url = "http://graph.facebook.com/{0}/picture?width={1}&height={1}"
            if len(fb_uid):
                picture_url = img_url.format(fb_uid[0].uid, picture_size)

    profile = UserProfile(user=user, avatar_url=picture_url)
    profile.save()
