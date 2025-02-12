from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView, TemplateView

from blog.forms import PostForm
from blog.models import BlogPost


class UserAccessMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        blogpost = BlogPost.objects.get(id=kwargs.get('pk'))
        owner_data = blogpost.user
        if blogpost.published_sign:
            return super().dispatch(request, *args, **kwargs)
        elif request.user == AnonymousUser():
            return render(request, 'newsletterapp/home.html')
        elif request.user != owner_data:
            return render(request, 'error_message.html')
        else:
            return super().dispatch(request, *args, **kwargs)


class BlogListView(ListView):
    model = BlogPost
    template_name = 'blog/blog_view.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(published_sign='pub')
        return queryset


class UserBlogListView(ListView):
    model = BlogPost

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Мой блог"
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(user=self.request.user.pk)
        return queryset


class PostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Новая публикация"
        return context

    def form_valid(self, form):
        if form.is_valid:
            print(self.request.FILES)
            obj = form.save()
            obj.user = self.request.user
            obj.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:all_posts')


class PostUpdateView(UserAccessMixin, UpdateView):
    model = BlogPost
    form_class = PostForm

    def get_success_url(self):
        return reverse('blog:read_post', args=[self.kwargs.get('pk')])


class ReadPostView(UserAccessMixin, DetailView):
    model = BlogPost

    def get_object(self, queryset=None):
        obj = super().get_object()
        obj.views_count += 1
        obj.save()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = kwargs.get('object').title
        return context


class PostDeleteView(UserAccessMixin, DeleteView):
    model = BlogPost

    def get_success_url(self):
        return reverse('blog:all_posts')


class ConfirmPublicationView(UserAccessMixin, TemplateView):
    template_name = 'blog/confirm_publication.html'

    def post(self, *args, **kwargs):
        blogpost = BlogPost.objects.get(id=kwargs.get('pk'))
        blogpost.published_sign = 'work'
        blogpost.save()

        return redirect('blog:read_post', pk=kwargs.get('pk'))


