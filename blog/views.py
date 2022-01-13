from django.shortcuts import render, get_object_or_404

from .models import Post

def post_list(request):
    """ A view to return the blog page"""

    """ to only show posts that are published"""

    posts = Post.objects.filter(status=1).order_by('created_on')

    template = 'blog/blog.html'
    
    context = {
        'posts': posts,
    }

    return render(request, template, context)

def post_detail(request, post_id):
    """ A view to return the blog details """

    specific_blog = request.GET.get('post_id')
    posts = Post.objects.filter(status=1).order_by('created_on')


    template = 'blog/post_detail.html'
    
    context = {
        'specific_blog': specific_blog,
        'posts':posts,
    }

    return render(request, template, context)



