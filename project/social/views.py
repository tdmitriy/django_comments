from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Comment, User
from .forms import FormPostComment
from .utils import *
import logging

index_template = 'social/index.html'

log = logging.getLogger(__name__)


def index(request):
    context = {
        'comment_post_form': FormPostComment(),
    }
    return render(request, index_template, context)


def json_comments(request, page, per_page):
    if request.is_ajax():
        if int(per_page) <= 0:
            return HttpResponseBadRequest('Bad request: per_page must be grater than 0')

        comments_set = Comment.objects.filter(root_id=None, parent_id=None)
        paginator = Paginator(comments_set, per_page)

        try:
            comments_page = paginator.page(page)
        except PageNotAnInteger:
            comments_page = paginator.page(1)
        except EmptyPage:
            comments_page = paginator.page(paginator.num_pages)

        comments_list = get_comments_and_replies(comments_page)

        return JsonResponse({
            'comments_list': get_comment_list_json(comments_list),
            'page': get_pageable_json(comments_page)
        }, safe=False)
    else:
        return HttpResponse('Only ajax calls are accepted.', status=403)


def comment_add(request):
    if request.method == 'POST':
        form = FormPostComment(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.content = form.cleaned_data.get('content')
            comment.user_id = 1
            comment.save()
            return HttpResponse('OK', {'comment': comment.as_json()})
        else:
            errors = form.errors
            log.exception("Could not save new reply. %s" % ','.join([str(error) for error in errors]))
            return HttpResponseBadRequest('Could not save new comment.')
    else:
        return HttpResponse('Only ajax calls are accepted.', status=403)
