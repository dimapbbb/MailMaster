from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import (UserBlogListView,
                        PostCreateView,
                        ReadPostView,
                        PostDeleteView,
                        PostUpdateView,
                        ConfirmPublicationView,
                        BlogListView)

app_name = BlogConfig.name

urlpatterns = [
    path('blog/', cache_page(60)(BlogListView.as_view()), name='blog'),
    path('user_blog/', UserBlogListView.as_view(), name='all_posts'),
    path('new_post/', PostCreateView.as_view(), name='new_post'),
    path('update_post/<int:pk>', PostUpdateView.as_view(), name='update_post'),
    path('read_post/<int:pk>', ReadPostView.as_view(), name='read_post'),
    path('delete_post/<int:pk>', PostDeleteView.as_view(), name='delete_post'),
    path('confirm_publication/<int:pk>', ConfirmPublicationView.as_view(), name='confirm_publication'),
]
