from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.CharField(max_length=128)

    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def as_json(self):
        return {
            "full_name": self.full_name(),
        }

    class Meta:
        db_table = "users"

    def __str__(self):
        return "User[%s, %s, %s]" % (self.first_name, self.last_name, self.email)


class Comment(models.Model):
    user = models.ForeignKey(User, null=False)
    root_id = models.IntegerField(null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True)
    content = models.TextField(null=False)
    pub_date = models.DateTimeField(null=False, auto_now_add=True)

    # field 'self.children' appended in 'utils.make_tree' function
    def as_json(self):
        return {
            "id": self.id,
            "user": self.user.as_json(),
            "root_id": self.root_id,
            "parent_id": self.parent_id,
            "children": [child.as_json() for child in self.children],
            "content": self.content,
            "pub_date": str(self.pub_date.strftime('%Y-%m-%d %H:%m'))
        }

    class Meta:
        db_table = 'comments'
        ordering = ['-pub_date']

    def __str__(self):
        # return "Comment[%d, %d, %s, %s, %s]" % (self.id, self.root_id, self.parent, self.content, self.pub_date)
        return "Comment[%s]" % self.content
