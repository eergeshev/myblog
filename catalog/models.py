from django.db import models
from django.urls import reverse

from datetime import date
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User #Blog author or commenter
from django.db.models.signals import post_save
from django.dispatch import receiver


   

class Blogger(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete = models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150, default=False)
    bio = models.TextField(max_length = 500, help_text = "Enter your bio here.")

    class Meta:
        ordering = [ 'user','bio']

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('blogger-detail', kwargs={
            'pk': self.pk
        })
    def get_full_name(self):
        return self.user.first_name + ' ' + self.user.last_name

    @receiver(post_save, sender=User)
    def update_blogger_signal(sender, instance, created, **kwargs):
        if created:
            Blogger.objects.create(user=instance)
        instance.blogger.save()

        



class Blog(models.Model):
    title = models.CharField(max_length = 200)
    post_date = models.DateField( default = date.today)
    author = models.ForeignKey(Blogger, on_delete = models.SET_NULL, null = True)
    description = models.TextField(max_length = 2000, help_text = "Enter your text here.")
    
    class Meta:
        ordering = ["-post_date"]

    def  __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog-detail', args=[str(self.id)])


class Comment(models.Model):
    
    author = models.ForeignKey(User,  on_delete = models.SET_NULL, null=True, default = False)
    body = models.TextField(max_length = 160, null = False, blank = False)
    post_date = models.DateTimeField(auto_now_add = True)
    post = models.ForeignKey(Blog,  on_delete = models.CASCADE, related_name = 'comments', null = True)

    class Meta:
        ordering = ["-post_date"]

    def __str__(self):
        return self.body
   
    
        