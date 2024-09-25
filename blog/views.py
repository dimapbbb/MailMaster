from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from blog.forms import PostForm
from blog.models import BlogPost


class BlogListView(ListView):
    model = BlogPost

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Мой блог"
        return context


class PostCreateView(CreateView):
    model = BlogPost
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Новая публикация"
        return context

    def form_valid(self, form):
        if form.is_valid:
            obj = form.save()
            obj.user = self.request.user
            obj.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:all_posts')


class PostUpdateView(UpdateView):
    model = BlogPost
    form_class = PostForm

    def get_success_url(self):
        return reverse('blog:read_post', args=[self.kwargs.get('pk')])


class ReadPostView(DetailView):
    model = BlogPost

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = kwargs.get('object').title
        return context


class PostDeleteView(DeleteView):
    model = BlogPost

    def get_success_url(self):
        return reverse('blog:all_posts')
