from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.paginator import Paginator, InvalidPage

from .models import Comment, User, Reply
from .forms import CommentAddForm
from .utils import *
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

index_template = 'social/index.html'
comments_template = 'social/comments.html'
comments_replies_template = 'social/comments_replies.html'
post_comment_template = 'social/comment_add.html'


def index(request):
    # if request.method == "POST":
    #     form = CommentAddForm(request.POST)
    #     if form.is_valid():
    #         comment = Comment()
    #         comment.content = form.cleaned_data.get('content')
    #         comment.user_id = 1
    #         comment.save()
    #     return redirect("social:index")

    items_per_page = 100
    comments_set = Comment.objects.all()
    paginator = Paginator(comments_set, items_per_page)

    form = CommentAddForm()

    try:
        page = paginator.page(1)
    except InvalidPage:
        raise Http404

    comments = get_comments_and_replies(page)
    context = {
        'comments_template': comments_template,
        'comments_replies_template': comments_replies_template,
        'post_comment_template': post_comment_template,
        'comments_list': comments,
        'form': form,
    }
    return render(request, index_template, context)


def comment_add(request):
    if request.method == "POST":
        form = CommentAddForm(request.POST)
        if form.is_valid():
            comment = Comment()
            comment.content = form.cleaned_data.get('content')
            comment.user_id = 1
            comment.save()

    return HttpResponseRedirect(reverse('social:index'), {'form': CommentAddForm()})
