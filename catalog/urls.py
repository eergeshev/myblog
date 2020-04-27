from django.urls import path
from . import views

urlpatterns = [
    path('blog', views.index, name = 'index'),
    path('blog/blogs/', views.BlogListView.as_view(), name = 'blogs'),
    path('blog/<int:pk>', views.BlogDetailView.as_view(), name = 'blog-detail'),
    path('blog/<int:pk>/update', views.BlogUpdate.as_view(), name = 'blog-update'),
     path('blog/<int:pk>/del', views.DeleteBlog.as_view(), name = 'delete-post')
]

urlpatterns += [
    path('blog/bloggers', views.BloggerListView.as_view(), name = 'bloggers'),
    path('blog/blogger/<int:pk>', views.BloggerDetailView.as_view(), name = 'blogger-detail'),
    path('blog/bloggerme/<int:pk>/', views.view_profile, name = 'profile-detail'),
    path('blog/bloggerme/<int:pk>/edit', views.edit_profile, name = 'edit-profile')
]
 
urlpatterns += [
    
    path('blog/<int:pk>/create/', views.comment_create, name = 'add-comment'),
    path('blog/bloggerme/<int:pk>/newpost/', views.new_post, name = 'new-post')
]

urlpatterns += [
    path('blog/register/', views.register, name = 'register')
]
