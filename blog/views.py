
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages

from .forms import PostForm, registrationform
from .models import Post, Category, Tag
from django.shortcuts import render


# Create a post (class-based view)
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    login_url = '/accounts/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user

        messages.success(
            self.request,
            'Post created successfully.'
        )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'slug': self.object.slug}
        )


# Register a user
class RegistrationView(CreateView):
    form_class = registrationform
    template_name = 'registration/register.html'
    success_url = '/'

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response



# Home page
def home(request):
    posts = Post.objects.filter(
        status='published'
    ).order_by('-created_at')

    paginator = Paginator(posts, 6)
    page_obj = paginator.get_page(
        request.GET.get('page')
    )

    categories = Category.objects.all().order_by('name')

    return render(
        request,
        'blog/home.html',
        {
            'posts': page_obj,
            'page_obj': page_obj,
            'categories': categories,
        }
    )



# About page
def about(request):
    return render(
        request,
        'blog/about.html',
        {'title': 'About'}
    )


# Contact page
def contact(request):
    return render(
        request,
        'blog/contact.html',
        {'title': 'Contact'}
    )


# List published posts
def post_list(request):
    posts = Post.objects.filter(
        status='published'
    ).order_by('-created_at')

    return render(
        request,
        'blog/post_list.html',
        {'posts': posts}
    )


# Display posts by category
def category_posts(request, category_id):
    category = get_object_or_404(
        Category,
        id=category_id
    )

    posts = Post.objects.filter(
        category=category,
        status='published'
    ).order_by('-created_at')

    return render(
        request,
        'blog/category_posts.html',
        {
            'category': category,
            'posts': posts,
        }
    )


# Post detail page
class PostdetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        published = Post.objects.filter(
            status='published'
        )

        if self.request.user.is_authenticated:
            return Post.objects.filter(
                Q(status='published') |
                Q(author=self.request.user)
            )

        return published


# Display a published post
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


# Create a post (function-based view)
@login_required(login_url='/accounts/login/')
def post_create(request):
    if request.method == 'POST':
        form = PostForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()

            messages.success(
                request,
                'Post created successfully.'
            )

            return redirect(
                'blog:post_detail',
                slug=post.slug
            )
    else:
        form = PostForm()

    return render(
        request,
        'blog/post_form.html',
        {'form': form}
    )


# Update a post
@login_required(login_url='/accounts/login/')
def post_update(request, slug):
    post = get_object_or_404(
        Post,
        slug=slug,
        author=request.user
    )

    if request.method == 'POST':
        form = PostForm(
            request.POST,
            request.FILES,
            instance=post
        )

        if form.is_valid():
            post = form.save()

            messages.success(
                request,
                'Post updated successfully.'
            )

            return redirect(
                'blog:post_detail',
                slug=post.slug
            )
    else:
        form = PostForm(instance=post)

    return render(
        request,
        'blog/post_form.html',
        {
            'form': form,
            'post': post,
        }
    )


# Delete a post
@login_required(login_url='/accounts/login/')
def post_delete(request, slug):
    post = get_object_or_404(
        Post,
        slug=slug,
        author=request.user
    )

    if request.method == 'POST':
        post.delete()

        messages.success(
            request,
            'Post deleted successfully.'
        )

        return redirect('blog:post_list')

    return render(
        request,
        'blog/post_confirm_delete.html',
        {'post': post}
    )


# Custom 403 Forbidden page
def custom_403(request, exception=None):
    return render(
        request,
        'blog/403.html',
        status=403
    )

# Test page for 403 error
from django.shortcuts import render

def test_403(request):
    return render(request, 'blog/403.html', status=403)
def custom_404(request, exception):
    return render(request, '404.html', status=404)
def error_500_demo(request):
    return render(request, '500.html', status=200)