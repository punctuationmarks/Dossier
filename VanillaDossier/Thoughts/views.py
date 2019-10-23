from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from Thoughts.models import ThoughtsModel


@login_required
def thoughts(request):
    """
    Adding a search bar at navbar
    """
    page_title = "thoughts"
    posts_list = ThoughtsModel.objects.order_by('title')
    search_term = ''
    
    if 'search' in request.GET:
        search_term = request.GET['search']
        orm_search = posts_list.filter(title__icontains=search_term) | posts_list.filter(body__icontains=search_term)
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
        'search_term': search_term
    }
    return render(request, 'Thoughts/thoughtsmodel.html', context)


class PostDetailView(DetailView):
    model = ThoughtsModel


class PostCreateView(LoginRequiredMixin, CreateView):
    model = ThoughtsModel
    fields = ['title', 'body']

    def form_valid(self, form):

        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ThoughtsModel
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
    model = ThoughtsModel
    # if everything goes well, this is a redirect url
    success_url = '/thoughts'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
