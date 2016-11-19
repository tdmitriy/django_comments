from .models import Comment


def make_tree(items):
    """
    WARNING: needs an ordering by 'parent_id' field
    Function that makes list-readable representation of tree from QuerySet
    :param items: given QuerySet
    :return: list of Comments tree
    """
    tree = []
    for item in items:
        item.children = []
        if item.parent_id is None:
            tree.append(item)
        else:
            try:
                parent = [p for p in items if p.id == item.parent_id][0]
                parent.children.append(item)
            except ValueError:
                tree.append(item)
    return tree


# TODO remove this class. Sadly that i wrote this class and it's useless anymore :(
class ThreadedComments(object):
    def __init__(self):
        self.all_comments = Comment.objects.all().order_by('-pub_date')
        self.comments = []
        self.replies = []

        self._prepare_comments()

    def _prepare_comments(self):
        """
        helper method that populates comments and replies
        :return:
        """

        for comment in self.all_comments:
            if comment.parent_id is None:
                self.comments.append(comment)
            else:
                self.replies.append(comment)

        # the current replies are sorted by asc, so reverse them
        self.replies.reverse()

    def _search_comment_replies(self, comment_id):
        """
        recursively search on comment replies
        :param id param to search:
        :return list of found replies:
        """

        result = []
        replies = list(filter(lambda r: r.parent_id == comment_id, self.replies))

        if replies:
            for reply in replies:
                result.append(reply)
                result.extend(self._search_comment_replies(reply.id))

        return result

    def get_comments(self):
        """
        :return list of comments with replies:
        """

        result = []

        for comment in self.comments:
            comment_replies = self._search_comment_replies(comment.id)
            result.append({comment: comment_replies})

        return result
