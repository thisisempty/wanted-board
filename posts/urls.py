from django.urls import path

from posts.views import PostView, PostDetailView
urlpatterns = [
    path('/register', PostView.as_view()),
    path('/<int:post_id>', PostView.as_view()),
    path('', PostView.as_view()),
    path('/detail', PostDetailView.as_view())
]