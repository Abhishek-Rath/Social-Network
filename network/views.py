from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required

from .models import User, Post, Follow

class PageList(ListView):
    paginate_by = 2
    model = Post

def index(request):
    if request.method == "POST":
        user = User.objects.get(username = request.user)
        content = request.POST["content"]

        post = Post()
        post.user = user
        post.content = content
        post.save()
        return redirect('index')

    if request.method == "GET":
        posts = Post.objects.all().order_by('-date')
        # posts = Post.objects.get_queryset().order_by('-date')

        paginator = Paginator(posts, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        print("\n\n", page_obj,"\n\n")
        return render(request, "network/index.html", {
            "posts":posts,
            'page_obj': page_obj
        })


    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def profile(request, user):
    profile_user = User.objects.filter(username = user).first()
    current_user = request.user
    # to get followers of user get the no. of users who are following the displayed user
    followers = len(Follow.objects.filter(following = profile_user))

    # TO get following, get no, of users the current user follows
    following = len(Follow.objects.filter(follower = profile_user))

    posts = Post.objects.filter(user = profile_user).order_by('-date')

    paginator = Paginator(posts, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    print(profile_user, current_user)

    is_following = Follow.objects.filter(follower = current_user, following = profile_user)

    # Check if logged in user follws the profile user
    if(is_following):
        follow_state = True
        return render(request, 'network/profile.html', {
            "username": profile_user,
            "followers": followers,
            "following": following,
            "page_obj": page_obj,
            "posts": posts,
            "follow_state":follow_state
        })
    else:
        follow_state = False
        return render(request, 'network/profile.html', {
            "username": profile_user,
            "followers": followers,
            "following": following,
            "page_obj": page_obj,
            "posts": posts,
            "follow_state":follow_state
        })



# @login_required
def following(request):
    if request.method == "POST":
        user = User.objects.get(username = request.user)
        content = request.POST["content"]

        post = Post()
        post.user = user
        post.content = content
        post.save()
     
    # Get the query set of people the logged in user follows 
    following_users = Follow.objects.filter(follower = request.user)

    # Get all the posts
    posts = Post.objects.all().order_by('-date')

    following_user_posts = list()

    for foll_user in following_users:
        for post in posts:
            if post.user == foll_user.following:
                following_user_posts.append(post)
        # print(foll_user.following.id)
    # print(following_users)
    print(following_user_posts)

    paginator = Paginator(following_user_posts, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "following_users":following_users,
        "following_user_posts":following_user_posts,
        "page_obj":page_obj,
    })  


@login_required(login_url = 'login')
def follow(request, user, curr_user):
    profile_user = User.objects.get(username = user)
    current_user = User.objects.get(username = curr_user)
   

    print("\n\n",profile_user,"\n\n")
    print("\n\n",current_user,"\n\n")

    # Current user follows profile user
    # follow_prof_user = Follow(follower = current_user, following = profile_user)
    # follow_prof_user.save()

    if(profile_user != current_user):

        following = Follow.objects.filter(follower = current_user, following = profile_user)
        follow_state = False

        # check if not already following
        if(not following): 
            # create new follow object
            follow_obj = Follow.objects.create(follower = current_user, following = profile_user) 
            
            # commit to db
            follow_obj.save() 
            
            print(f"{current_user} follows {profile_user}")
        else:
            following.delete()
            print(f"{current_user} unfollwed {profile_user}")
        # return redirect('profile', user = profile_user)
        return HttpResponse("")