from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

from .models import Post
from .forms import PostForm


def home(request):
    posts = Post.objects.filter(
        status='published'
    ).order_by('-created_at')

    paginator = Paginator(posts, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/home.html',
        {
            'posts': page_obj,
            'page_obj': page_obj,
        }
    )


def about(request):
    return render(
        request,
        'blog/about.html',
        {'title': 'About'}
    )


def contact(request):
    return render(
        request,
        'blog/contact.html',
        {'title': 'Contact'}
    )


# List all published posts
def post_list(request):
    posts = Post.objects.filter(
        status='published'
    ).order_by('-created_at')

    return render(
        request,
        'blog/post_list.html',
        {'posts': posts}
    )


# Display a single post
def post_detail(request, slug):
    post = get_object_or_404(
        Post,
        slug=slug,
        status='published'
    )

    return render(
        request,
        'blog/post_detail.html',
        {'post': post}
    )


# Create a new post
def post_create(request):
    if request.method == 'POST':
        form = PostForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            form.save()
            return redirect('blog:post_list')
    else:
        form = PostForm()

    return render(
        request,
        'blog/post_form.html',
        {'form': form}
    )


# Update an existing post
def post_update(request, slug):
    post = get_object_or_404(
        Post,
        slug=slug
    )

    if request.method == 'POST':
        form = PostForm(
            request.POST,
            request.FILES,
            instance=post
        )

        if form.is_valid():
            form.save()
            return redirect(
                'blog:post_detail',
                slug=post.slug
            )
    else:
        form = PostForm(
            instance=post
        )

    return render(
        request,
        'blog/post_form.html',
        {
            'form': form,
            'post': post,
        }
    )


# Delete an existing post
def post_delete(request, slug):
    post = get_object_or_404(
        Post,
        slug=slug
    )

    if request.method == 'POST':
        post.delete()
        return redirect('blog:post_list')

    return render(
        request,
        'blog/post_confirm_delete.html',
        {'post': post}
    )
