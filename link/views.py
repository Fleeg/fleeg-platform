from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from account.models import Account
from link.utils import LinkException
from link.forms import URLForm
from link.models import Post


class LinkView:
    @staticmethod
    def links(request, username):
        posts = Post.objects.filter(owner__user__username=username).order_by('-created_at')
        profile = get_object_or_404(User, username=username)
        profile_account = Account.get_by_user(user=profile)
        if request.user.is_authenticated:
            session_account = Account.get_by_user(request.user)
            request.user.is_following = session_account.is_following(profile_account)
        return render(request, 'link/link.html', {'profile': profile, 'posts': posts})

    @staticmethod
    @login_required
    def new(request):
        form = None
        if request.method == 'POST':
            form = URLForm(request.POST)
            if form.is_valid():
                link = form.save(commit=False)
                link.owner = Account.get_by_user(request.user)
                link.publisher = Account.get_by_user(request.user)
                try:
                    link.set_metadata()
                    link.save()
                    return redirect('home')
                except LinkException as e:
                    form.add_error(None, e)
        return render(request, 'home.html', {'form': form})

    @staticmethod
    @login_required
    def wall(request):
        owner = request.user.accounts.first()
        posts = owner.posts.all().order_by('-created_at')
        return render(request, 'home.html', {'posts': posts})
