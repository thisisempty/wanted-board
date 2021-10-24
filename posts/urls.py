from django.urls import path

from posts.views import PostView

urlpatterns = [
    path('/register', PostView.as_view()),
    path('/<int:post_id>', PostView.as_view()),
    path('', PostView.as_view())
]