from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from account.forms import SignUpForm, LoginForm
from account.models import Account, Relationship


class AuthView:
    @staticmethod
    def signup(request):
        form = None
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form_user = form.save(commit=False)
                user = User.objects.create_user(username=form_user.username, email=form_user.email,
                                                password=form_user.password,)
                user.first_name = form_user.first_name
                user.last_name = form_user.last_name
                user.save()
                account = Account(user=user)
                account.save()
        return render(request, 'index.html', {'formSignUp': form})

    @staticmethod
    def login(request):
        form = None
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                data = form.data
                if '@' in data['identity']:
                    kwargs = {'email': data['identity'].lower()}
                else:
                    kwargs = {'username': data['identity'].lower()}
                try:
                    user = User.objects.get(**kwargs)
                    if user is not None and user.check_password(data['password']):
                        login(request, user)
                        if 'keep_connected' in data:
                            request.session.set_expiry(0)
                        return redirect(reverse('home'))
                except User.DoesNotExist:
                    pass
        return render(request, 'index.html', {'form': form})

    @staticmethod
    def home_redirect(request):
        if request.user.is_authenticated():
            return redirect(reverse('home'))
        else:
            return render(request, 'index.html')

    @staticmethod
    @login_required
    def logout_redirect(request):
        logout(request)
        return redirect(reverse('index'))


class ProfileView:
    @staticmethod
    def posts(request, username):
        profile = get_object_or_404(User, username=username)
        profile_account = Account.get_by_user(user=profile)
        posts = profile_account.posts.all()
        if request.user.is_authenticated:
            session_account = Account.get_by_user(request.user)
            request.user.is_following = session_account.is_following(profile_account)
        return render(request, 'profile.html', {'profile': profile, 'posts': posts})

    @staticmethod
    def following(request, username):
        users = User.objects.filter(accounts__followers__owner__user__username=username)
        profile = get_object_or_404(User, username=username)
        profile_account = Account.get_by_user(user=profile)
        if request.user.is_authenticated:
            session_account = Account.get_by_user(request.user)
            request.user.is_following = session_account.is_following(profile_account)
        return render(request, 'account/user.html', {'profile': profile, 'users': users})

    @staticmethod
    def followers(request, username):
        users = User.objects.filter(accounts__following__follow__user__username=username)
        profile = get_object_or_404(User, username=username)
        profile_account = Account.get_by_user(user=profile)
        if request.user.is_authenticated:
            session_account = Account.get_by_user(request.user)
            request.user.is_following = session_account.is_following(profile_account)
        return render(request, 'account/user.html', {'profile': profile, 'users': users})

    @staticmethod
    @login_required
    def follow(request, username):
        if request.method == 'POST':
            relationship = Relationship()
            relationship.owner = Account.get_by_user(request.user)
            relationship.follow = Account.get_by_username(username)
            if not relationship.owner.is_following(relationship.follow):
                relationship.save()
            return redirect('profile', username)

    @staticmethod
    @login_required
    def unfollow(request, username):
        if request.method == 'POST':
            owner = Account.get_by_user(request.user)
            follow = Account.get_by_username(username)
            owner.unfollow(follow)
            return redirect('profile', username)
