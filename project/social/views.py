from django.http import HttpResponse
from django.shortcuts import render

from .models import Comment
from .utils import make_tree


def index(request):
    comment_list = Comment.objects.all()
    comment_tree = make_tree(comment_list)

    return render(request, "social/comment_tree.html", {'comments': comment_tree})
    # return HttpResponse("Hello, world. You're at the comments page.")


def comments(request):
    # return render(request, "social/comments.html", {'nodes': Comment.objects.all()})
    return HttpResponse("Hello, world. You're at the comments page.")
