from django.shortcuts import render

from .models import Post

class post_list(generic.ListView):
    show_published_posts = Post.objects.filter(status=1).order_by('created_on')
    template = 'blog.html'
    
    return render(template)

class post_detail(generic.DetailView):
    model = Post
    template = 'post_detail.html'

    return render(template)

