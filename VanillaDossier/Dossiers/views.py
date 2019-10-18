from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from Dossiers.models import DossiersModel


@login_required
def dossiers(request):
    """
    Adding a search bar at navbar
    """
    page_title = "dossiers"
    posts_list = DossiersModel.objects.order_by('name')
    search_term = ''

    if 'search' in request.GET:
        search_term = request.GET['search']
        posts = posts_list.filter(name__icontains=search_term)
    else:
        posts = posts_list

    page = request.GET.get('page', 1)

    paginator = Paginator(posts, 5)

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
    return render(request, 'Dossiers/dossiers.html', context)


class PostDetailView(DetailView):
    model = DossiersModel


class PostCreateView(LoginRequiredMixin, CreateView):
    model = DossiersModel
    fields = ['name', 'hobbies', 'work', 'appearance', 'toRemember', 'discussions']

    def form_valid(self, form):

        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = DossiersModel
    fields = ['name', 'hobbies', 'work', 'appearance', 'toRemember', 'discussions']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # ensuring the correct author is the one updating
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = DossiersModel
    # if everything goes well, this is a redirect url
    success_url = '/dossiers'


    # ensuring the correct author is the one deleting
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
