from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import PostForm, ImageFormSet
from .models import Post, Like, Image
from accounts.models import Subscription
from django.views.decorators.http import require_POST


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # Ensure many-to-many relationships are saved
            form.save_tags(post)  # Explicitly call to ensure tags are saved
            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get(
                        'DELETE', False):
                    image = form.cleaned_data.get('image_file')
                    if image:
                        Image.objects.create(post=post, image_file=image)
            return redirect('posts:feed')
    else:
        form = PostForm()
        formset = ImageFormSet(queryset=Image.objects.none())
    return render(request, 'posts/post_create.html',
                  {'form': form, 'formset': formset})


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/post_detail.html', {'post': post})


@login_required
def friends_feed(request):
    subscriptions = Subscription.objects.filter(subscriber=request.user)
    subscribed_users = [sub.subscribed_to for sub in subscriptions]
    posts = Post.objects.filter(author__in=subscribed_users).order_by('-date_posted')
    return render(request, 'posts/friends_feed.html', {'posts': posts, 'subscribed_users': subscribed_users})

@login_required
def feed(request):
    subscriptions = Subscription.objects.filter(subscriber=request.user)
    subscribed_users = [sub.subscribed_to for sub in subscriptions]
    posts = Post.objects.all().order_by('-date_posted')
    return render(request, 'posts/feed.html', {'posts': posts, 'subscribed_users': subscribed_users})

@require_POST
@login_required
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    liked = False
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    else:
        liked = True
    return JsonResponse({'liked': liked, 'total_likes': post.liked_by.count()})
