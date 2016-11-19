from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.CharField(max_length=128)

    class Meta:
        db_table = "users"

    def __str__(self):
        return "User[%s, %s, %s]" % (self.first_name, self.last_name, self.email)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    parent = models.ForeignKey('self', blank=True, null=True)
    content = models.CharField(max_length=512, null=False)
    pub_date = models.DateTimeField(null=False, auto_now_add=True)

    class Meta:
        db_table = "comments"

        ordering = ['parent_id', '-pub_date']

    def __str__(self):
        return "Comment[%d, %s, %s, %s]" % (self.id, self.parent, self.content, self.pub_date)
