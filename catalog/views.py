from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from .models import Comment, Blogger, Blog
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin    
from .forms import CommentForm, EditBloggerForm, EditUserForm, SelfBlogForm, SignUpForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, authenticate
# Create your views here.

def index(request):
    # blogger_count = Blogger.objects.all().count()
    blog_count = Blog.objects.all().count()
    comment_count = Comment.objects.all().count()

    context = {
                'blog_count': blog_count,
                'comment_count': comment_count
                }
    return render(request, 'index.html', context = context)

  

def register(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.blogger.first_name = form.cleaned_data.get('first_name')
        user.blogger.last_name = form.cleaned_data.get('last_name')
        user.blogger.email = form.cleaned_data.get('email')
        user.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/register_form.html', {'form': form})


class BlogListView( generic.ListView):
    model = Blog
    

class BlogDetailView( generic.DetailView):
    model = Blog
    

class BlogUpdate(UpdateView):
    model = Blog
    fields = ('title', 'description')

class DeleteBlog(DeleteView):
    model = Blog
    success_url = reverse_lazy('index')

class BloggerListView( generic.ListView):
    model = Blogger
    

class BloggerDetailView( generic.DetailView):
    model = Blogger

@login_required
def comment_create(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    user_ = Blogger.objects.get(user = request.user)
    if request.method == "POST":
        
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog-detail', pk=post.pk)
    else:
        form = CommentForm()
        context = {
            'form': form,
            'post': post,
            'user': request.user.username
        }
        return render(request, 'catalog/create_comment.html', context )


@login_required
def view_profile(request,pk):
    user= get_object_or_404(User, pk = pk)
    blogger = user.blogger
      
    args = {'user': user,
             'blogger': blogger,
            }
    return render(request, 'catalog/profile_detail.html', args)


@login_required
def edit_profile(request, pk):
   
    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance = request.user)
        blogger_form = EditBloggerForm(request.POST, instance = request.user.blogger)

        if user_form.is_valid and blogger_form.is_valid():
            user_form.save()
            blogger_form.save()
        return redirect('profile-detail', pk = request.user.id)
    else:
        user_form = EditUserForm(instance = request.user)
        blogger_form = EditBloggerForm(instance = request.user.blogger)
        context = {
            'user_form': user_form,
            'blogger_form': blogger_form

        }
        return render(request, 'catalog/edit_profile.html', context)


def new_post(request, pk):
        
    if request.method == 'POST':
        user_ = Blogger.objects.get(user = request.user)
        form = SelfBlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit = False)
            blog.author = user_
            blog.save()
            return redirect('profile-detail', pk=request.user.id)
    else:
        form = SelfBlogForm()
        return render(request, 'catalog/new_post.html', {'form': form})
