from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import render
from django.core.paginator import Paginator, InvalidPage

from .models import Comment, User, Reply
from .forms import FormPostComment, FormReplyToComment
from .utils import *
from django.shortcuts import redirect
import logging

index_template = 'social/index.html'
comments_list_template = 'social/comments_list.html'
comments_replies_list_template = 'social/comments_replies_list.html'
comment_post_template = 'social/comment_post.html'
comment_reply_template = 'social/comment_reply.html'

log = logging.getLogger(__name__)


def index(request):
    items_per_page = 3
    comments_set = Comment.objects.all()
    paginator = Paginator(comments_set, items_per_page)

    comment_post_form = FormPostComment()
    comment_reply_form = FormReplyToComment()

    try:
        page = paginator.page(1)
    except InvalidPage:
        raise Http404

    comments = get_comments_and_replies(page)
    context = {
        'comments_list_template': comments_list_template,
        'comments_replies_list_template': comments_replies_list_template,
        'comment_post_template': comment_post_template,
        'comment_reply_template': comment_reply_template,

        'comments_list': comments,

        'comment_post_form': comment_post_form,
        'comment_reply_form': comment_reply_form,
    }
    return render(request, index_template, context)


def comment_add(request):
    if request.method == "POST":
        form = FormPostComment(request.POST)
        if form.is_valid():
            comment = Comment()
            comment.content = form.cleaned_data.get('content')
            comment.user_id = 1
            comment.save()

    return redirect('social:index')


def comment_reply(request):
    if request.method == "POST":
        form = FormReplyToComment(request.POST)
        try:
            if form.is_valid():
                comment_id = request.POST['comment_id']
                parent_id = request.POST['parent_id']

                reply = Reply()
                reply.comment_id = int(comment_id)
                reply.parent_id = None if parent_id.lower() in ['', 'none'] else int(parent_id)
                reply.content = form.cleaned_data.get('content')
                reply.user_id = 1
                reply.save()
        except (IntegrityError, ValueError) as ex:
            log.exception("Could not save new reply. %s" % str(ex))

    return redirect('social:index')
