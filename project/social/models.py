from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, related_name='profile')
    avatar_url = models.CharField(max_length=256, blank=True, null=True)

    def full_name(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

    class Meta:
        db_table = "user_profile"

    def __str__(self):
        return "UserProfile[%d, %s]" % (self.user_id, self.full_name())


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
