from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from django.views.generic import TemplateView
from django.shortcuts import render
from .forms import FormPostComment, FormReplyToComment
from .utils import CommentUtils
from .models import Comment, Reply

import logging

log = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = 'social/index.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        comments_per_page = 10
        page = request.GET.get('page')

        comment_post_form = FormPostComment()
        comment_reply_form = FormReplyToComment()

        comments_pageable = CommentUtils.get_comments_pageable(page=page, per_page=comments_per_page)
        comments_dict = CommentUtils.get_comments(comments_pageable)

        context['comment_post_form'] = comment_post_form
        context['comment_reply_form'] = comment_reply_form
        context['comments_dict'] = comments_dict
        context['comments_pageable'] = comments_pageable
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class CommentAddView(CreateView):
    model = Comment
    form_class = FormPostComment
    http_method_names = ['post']

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super(CommentAddView, self).form_valid(form)

    def form_invalid(self, form):
        errors = form.errors
        log.error("Could not save new comment. %s" % ','.join([str(error) for error in errors]))
        return super(CommentAddView, self).form_invalid(form)

    def get_success_url(self):
        return reverse('social:index')


@method_decorator(login_required, name='dispatch')
class CommentReplyView(CreateView):
    model = Reply
    form_class = FormReplyToComment
    http_method_names = ['post']

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super(CommentReplyView, self).form_valid(form)

    def form_invalid(self, form):
        errors = form.errors
        log.error("Could not save new reply. %s" % ','.join([str(error) for error in errors]))
        return super(CommentReplyView, self).form_invalid(form)

    def get_success_url(self):
        return reverse('social:index')
