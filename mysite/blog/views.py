from django.http import HttpResponseRedirect, request
from blog.forms import PostForm, CommentForm, UserForm, UserProfileInfoForm
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from blog.models import Post, Comment, UserProfileInfo
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth import authenticate,login,logout
from django.utils import timezone

# Create your views here.
class SignupView(View):
    def get(self, request):
        form = UserForm()
        return(render(request,'registration/signup.html',{'form':form}))

    def post(self, request):
        form = UserForm(request.POST)
        email = request.POST.get('email')
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        if form.is_valid() and email != "" and fname != "" and lname != "":
            user = form.save(commit=False)
            user.set_password(user.password)  
            user.save()
            form2 = UserProfileInfo(id=user.pk,user=user)
            form2.save()
            return(redirect('login'))
        else:
            return(render(request,'registration/signup.html',{'form':form,'message':"All fields are required"}))

class LoginView(View):
    def get(self, request):
        return(render(request,'registration/login.html'))

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            # User is authenticated
            if user.is_active:
                login(request,user)
                if request.POST.get('next') != '':
                    return HttpResponseRedirect(request.POST.get('next'))
                else:
                    return(redirect('post_list'))
            else:
                return(render(request,'registration/login.html',{'message':"Acoount is not active"}))
        else:
            return(render(request,'registration/login.html',{'message':"Incorrect Username or Password"}))

@login_required
def log_out(request):
    logout(request)
    return(redirect('post_list'))          

class UserProfileInfoDetailView(DetailView):
    model = UserProfileInfo
    template_name = "registration/profile.html"
    

class AboutView(TemplateView):
    template_name = 'blog/about.html'

class PostListView(ListView):
    model = Post
    def get_queryset(self):
        return(Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date'))
        #lte -> less than or equal to
        # '-' in -published_date is used to represent descending order

class UserDetailView(DetailView):
    model = User
    template_name = "blog/user_detail.html"

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.published_date = timezone.now()
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post


class UserProfileInfoUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'registration/profile.html'
    model = UserProfileInfo
    form_class = UserProfileInfoForm

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('post_myposts_list')

class MypostsListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    model = Post
    template_name = 'blog/myposts_list.html'
    def get_queryset(self):
        return(Post.objects.filter(author=self.request.user).order_by('-published_date'))

@login_required
def add_comment_to_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post 
            comment.create_date = timezone.now()
            comment.author = request.user
            comment.save()
            return(redirect('post_detail',pk=post.pk))
    else:
        form = CommentForm()
    return(render(request,'blog/comment_form.html',context={'form':form}))

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk 
    comment.delete()
    return(redirect('post_detail',pk=post_pk))