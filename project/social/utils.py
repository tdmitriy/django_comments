from .models import Comment
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


def get_comments_and_replies(page):
    """
    1) Take the ids of comments from the page object
    2) Filter replies with given comments ids
    3) Create a dictionary with filtered replies on each comment
    4) Make the final JSON with page info and dictionary of comments:
    { 'has_next': True/False, 'comments': {comment: list_of_replies} }
    :param page:
    :return dictionary like {comment: list_of_replies}:
    """

    result = []
    comments = page.object_list
    comment_ids = comments.values_list('id', flat=True)

    comment_replies = Comment.objects.filter(root_id__in=comment_ids).order_by('parent_id', 'pub_date')
    replies_tree = make_tree(comment_replies)

    for c in comments:
        c.children = [reply for reply in replies_tree if reply.root_id == c.id]
        result.append(c)

    return result


def get_pageable_json(page):
    return {
        "num_pages": page.paginator.num_pages,
        "page_number": page.number,
        "has_prev": bool(page.has_previous()),
        "has_next": bool(page.has_next()),
    }


def get_comment_list_json(comments_list):
    return [comment.as_json() for comment in comments_list]
