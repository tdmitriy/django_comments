from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Comment
from .forms import FormPostComment, FormReplyToComment
from .utils import *
from django.shortcuts import redirect
import logging

log = logging.getLogger(__name__)


def index(request):
    items_per_page = 10
    comments_set = Comment.objects.all()
    paginator = Paginator(comments_set, items_per_page)

    comment_post_form = FormPostComment()
    comment_reply_form = FormReplyToComment()

    page = request.GET.get('page')

    try:
        comments_page = paginator.page(page)
    except PageNotAnInteger:
        comments_page = paginator.page(1)
    except EmptyPage:
        comments_page = paginator.page(paginator.num_pages)

    comments_dict = get_comments(comments_page)
    context = {
        'comments_dict': comments_dict,
        'comments_page': comments_page,
        'comment_post_form': comment_post_form,
        'comment_reply_form': comment_reply_form,
    }
    return render(request, 'social/index.html', context)


@login_required
def comment_add(request):
    if request.method == "POST":
        form = FormPostComment(request.POST)
        if form.is_valid():
            comment = Comment()
            comment.content = form.cleaned_data.get('content')
            comment.user_id = request.user.id
            comment.save()
        else:
            errors = form.errors
            log.exception("Could not save new comment. %s" % ','.join([str(error) for error in errors]))

    return redirect('social:index')


@login_required
def comment_reply(request):
    if request.method == "POST":
        form = FormReplyToComment(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.content = form.cleaned_data.get('content')
            reply.comment_id = form.cleaned_data.get('comment_id')
            reply.parent_id = form.cleaned_data.get('parent_id')
            reply.user_id = request.user.id
            reply.save()
        else:
            errors = form.errors
            log.exception("Could not save new reply. %s" % ','.join([str(error) for error in errors]))

    return redirect('social:index')
