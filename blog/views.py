from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from .forms import EmailPostForm, CommentForm
from django.views.decorators.http import require_POST



def post_list(request):
    post_list = Post.published.all()

    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try: 
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)

    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context = {
        'posts': posts
    }

    return render(request, 'blog/post/list.html', context=context)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        status= Post.Status.PUBLISHED
    )
    comments = post.comments.filter(active=True)
    form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form
    }
    
    return render(request, 'blog/post/detail.html', context=context)


def post_share(request, post_id):
    post = get_object_or_404(Post,
        id=post_id,
        status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
        post_url = request.build_absolute_uri(
            post.get_absolute_url())
        subject = f"{cd['name']} recommends you read " \
            f"{post.title}"
        message = f"Read {post.title} at {post_url}\n\n" \
            f"{cd['name']}\'s comments: {cd['comments']}"
        send_mail(subject, message, 'asherzod2197@gmail.com',
            [cd['to']])
        sent = True
    else:
        form = EmailPostForm()
    context = {
        'post': post,
        'form': form,
        'sent': sent
    }

    return render(request, 'blog/post/share.html', context=context)


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )

    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    context = {
        'post': post,
        'form': form,
        'comment': comment
    }
    
    return render(request, 'blog/post/comment.html', context=context)
