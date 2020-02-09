from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from Ideas.models import IdeasModel

# sqs = SearchQuerySet().models(Product).order_by("company_name").extra(select={'company_name': 'lower(company_name)'}).order_by('company_name')


@login_required()
def ideas(request):

    page_title = "Ideas"
    # making all of the titles lower case (which is an asthetic)
    # and ordering them alphabetically

    # this has failing errors, when testing. Seems like I'll have better controll if I build
    # the form custom
    # posts_list = IdeasModel.objects.filter(author=request.user).extra(
    #     select={'title': 'lower(title)'}).order_by('title')

    # having the title's be ordered alphabetically, but if first letter is capitalized
    # then it'll order that one first
    posts_list = IdeasModel.objects.filter(
        author=request.user).order_by('title')
    
    search_term = ''

    if 'search' in request.GET:
        search_term = request.GET['search']
        orm_search = posts_list.filter(
            title__icontains=search_term) | posts_list.filter(body__icontains=search_term)
        posts = orm_search
    else:
        posts = posts_list
    page = request.GET.get('page', 1)

    paginator = Paginator(posts, 10)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'title': page_title,
        'posts': posts,
        'search_term': search_term,
        'is_paginated': bool(paginator.num_pages > 1),
        'num_of_pages': paginator.num_pages
    }

    return render(request, 'Ideas/ideasmodel.html', context)


class PostDetailView(DetailView):
    model = IdeasModel


class PostCreateView(LoginRequiredMixin, CreateView):
    model = IdeasModel
    fields = ['title', 'body']

    def form_valid(self, form):

        form.instance.author = self.request.user
        # form.instance.title = self.request.title.to_lower()
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = IdeasModel
    fields = ['title', 'body']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = IdeasModel
    # if everything goes well, this is a redirect url
    success_url = '/ideas'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
