from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from account.models import Account
from link.utils import LinkException
from link.forms import URLForm, CommentForm
from link.models import Post, Reaction


class LinkView:
    @staticmethod
    def links(request, username):
        session_account = None
        profile = get_object_or_404(User, username=username)
        profile_account = Account.get_by_user(user=profile)
        if request.user.is_authenticated:
            session_account = Account.get_by_user(request.user)
            request.user.is_following = session_account.is_following(profile_account)
        posts = Post.list_with_actions(username, session_account)
        return render(request, 'link/link.html', {'profile': profile, 'posts': posts})

    @staticmethod
    @login_required
    def wall(request):
        owner = request.user.accounts.first()
        posts = Post.list_with_actions(request.user.username, owner)
        return render(request, 'home.html', {'posts': posts})

    @staticmethod
    @login_required
    def new(request):
        form = None
        if request.method == 'POST':
            form = URLForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                user_account = Account.get_by_user(request.user)
                post.owner = user_account
                post.publisher = user_account
                try:
                    post.set_metadata()
                    post.save()
                    return redirect('home')
                except LinkException as e:
                    form.add_error(None, e)
        return render(request, 'home.html', {'form': form})

    @staticmethod
    @login_required
    def add(request, post_id):
        if request.method == 'POST':
            post = Post.objects.get(id=post_id)
            account = Account.get_by_user(request.user)
            post.add_link(account)
        redirect_path = request.GET['next']
        return redirect(redirect_path)


class LinkReactionView:
    @staticmethod
    @login_required
    def react(request, post_id):
        if request.method == 'POST':
            reaction = Reaction()
            reaction.post = Post.objects.get(id=post_id)
            reaction.owner = Account.get_by_user(request.user)
            reaction.save()
        redirect_path = request.GET['next']
        return redirect(redirect_path)

    @staticmethod
    @login_required
    def unreact(request, post_id):
        if request.method == 'POST':
            reaction = Reaction.objects.filter(post__id=post_id, owner__user=request.user).first()
            reaction.delete()
        redirect_path = request.GET['next']
        return redirect(redirect_path)


class LinkCommentView:
    @staticmethod
    @login_required
    def comment(request, post_id):
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = Post.objects.get(id=post_id)
                comment.owner = Account.get_by_user(request.user)
                comment.save()
        redirect_path = request.GET['next']
        return redirect(redirect_path)
