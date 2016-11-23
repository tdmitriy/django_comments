from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.CharField(max_length=128)

    def get_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    class Meta:
        db_table = "users"

    def __str__(self):
        return "User[%s, %s, %s]" % (self.first_name, self.last_name, self.email)


class Comment(models.Model):
    user = models.ForeignKey(User, null=False)
    content = models.TextField(null=False)
    pub_date = models.DateTimeField(null=False, auto_now_add=True)

    class Meta:
        db_table = 'comments'
        ordering = ['-pub_date']

    def __str__(self):
        return "Comment[%d, %s, %s]" % (self.id, self.content, self.pub_date)


class Reply(models.Model):
    user = models.ForeignKey(User, null=False)
    comment = models.ForeignKey(Comment, null=False)
    parent = models.ForeignKey('self', null=True, blank=True)
    content = models.TextField(null=False)
    pub_date = models.DateTimeField(null=False, auto_now_add=True)

    class Meta:
        db_table = 'replies'

        ordering = ['parent_id', 'pub_date']

    def __str__(self):
        return "Reply[%d, %d, %s, %s, %s]" % (self.id, self.comment_id, self.parent_id, self.content, self.pub_date)
