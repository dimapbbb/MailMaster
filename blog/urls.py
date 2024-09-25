from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogListView, PostCreateView, ReadPostView, PostDeleteView, PostUpdateView

app_name = BlogConfig.name

urlpatterns = [
    path('blog/', BlogListView.as_view(), name='all_posts'),
    path('new_post/', PostCreateView.as_view(), name='new_post'),
    path('update_post/<int:pk>', PostUpdateView.as_view(), name='update_post'),
    path('read_post/<int:pk>', ReadPostView.as_view(), name='read_post'),
    path('delete_post/<int:pk>', PostDeleteView.as_view(), name='delete_post'),
]
