from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CommentForm

def post_list(request):
    posts = Post.published.all()
    
    paginator = Paginator(posts, 10) # 10 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    return render(request, 'blog/post_list.html', {'posts':posts, page:'pages'})

def post_detail(request, post):
    post = get_object_or_404(Post, slug=post, status='published')
    
    comments = post.comments.filter(acitve=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect(post.get_absolute_url() + '#' + str(new_comment.id))
        else:
            comment_form = CommentForm()

    return render(request, 'blog/post_detail.html', {'post':post})


