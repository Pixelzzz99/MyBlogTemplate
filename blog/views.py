from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
    return render(request, 'blog/post_detail.html', {'post':post})

