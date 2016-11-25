from .models import Reply
from collections import OrderedDict


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


def get_comments(page):
    """
    1) Take the ids of comments from the page object
    2) Filter replies with given comments ids
    3) Create a dictionary with filtered replies on each comment
    4) Make the final JSON with page info and dictionary of comments:
    { 'has_next': True/False, 'comments': {comment: list_of_replies} }
    :param page:
    :return dictionary like {comment: list_of_replies}:
    """

    result = OrderedDict()
    comments = page.object_list
    comment_ids = comments.values_list('id', flat=True)

    comment_replies = Reply.objects.filter(comment_id__in=comment_ids)
    replies_tree = make_tree(comment_replies)

    for c in comments:
        result[c] = [reply for reply in replies_tree if reply.comment_id == c.id]

    return result
