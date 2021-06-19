from django.urls import path
from blog.views import AboutView, PostListView, PostDetailView, SignupView, LoginView
from blog.views import PostCreateView, PostUpdateView, PostDeleteView, MypostsListView, UserDetailView, UserProfileInfoDetailView,UserProfileInfoUpdateView
from blog.views import add_comment_to_post, comment_remove, log_out
urlpatterns = [
    path('',PostListView.as_view(),name="post_list"),
    path('signup/',SignupView.as_view(),name="signup"),
    path('login/',LoginView.as_view(),name="login"),
    path('logout/',log_out,name="logout"),
    path('profile/<pk>/',UserProfileInfoDetailView.as_view(),name="my_profile"),
    path('about/',AboutView.as_view(),name="about"),
    path('post/new/',PostCreateView.as_view(),name="post_new"),
    path('post/<pk>/',PostDetailView.as_view(),name="post_detail"),
    path('author/<pk>/detail',UserDetailView.as_view(),name="user_detail"),
    path('post/<pk>/edit',PostUpdateView.as_view(),name="post_edit"),
    path('user/<pk>/edit',UserProfileInfoUpdateView.as_view(),name="user_edit"),
    path('post/<pk>/remove',PostDeleteView.as_view(),name="post_remove"),
    path('my_posts',MypostsListView.as_view(),name="post_myposts_list"),
    path('post/<pk>/comment',add_comment_to_post,name="add_comment_to_post"),
    path('comment/<pk>/remove',comment_remove,name="comment_remove"),
]