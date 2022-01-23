from django.shortcuts import render, get_object_or_404

from .forms import CommentForm
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

    template = 'blog/post_detail.html'
    blog = get_object_or_404(Post, pk=post_id)
    comments = blog.comments.filter(active=True)
    new_comment = None

    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = blog
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    
    context = {
        'blog': blog,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    }

    return render(request, template, context)




