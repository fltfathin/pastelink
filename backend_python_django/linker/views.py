from django.shortcuts import render, redirect
from .models import Link
from django.views.generic import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import os
import secrets
import urllib
from django.utils.http import urlencode
import requests
import re

url_re = re.compile(
    r"(http[s]?://)?(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
)


# Create your views here.

def shortlink_view(request, shortlink):
    try:
        link = Link.objects.get(shortlink=shortlink)
    except Exception as e:
        return render(request, "linker/error.html", context={"error":e})
    return redirect(link.url)


def handle_callback(request):
    return render(request, "linker/login.html")


class LoginView(View):
    def get(self, request):
        params = {
            "client_id":"6c8a998f2fc6a1cac9bc",
            "redirect_url":"http://localhost:8000/login/oauth_callback",
            "scope": "user:email"
        }
        github_url = f"https://github.com/login/oauth/authorize?{urlencode(params)}" 
        return render(request, "linker/login.html", context={"github_url":github_url})

    def post(self, request):
        username, password = [request.POST.get(x) for x in ["username", "password"]]
        res = authenticate(request, username=username, password=password)
        if res is not None:
            login(request,res)
            return redirect("/")
        return render(request, "linker/login.html", context={"error":"wrong authentication"})

class Links(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'rel'

    def get(self, request):
        context = {"links":Link.objects.filter(owner=request.user)}
        return render(request, "linker/link_list.html", context=context)

    def post(self, request):
        url, shortlink = [request.POST.get(x) for x in ["url", "shortlink"]]
        context = {"links":Link.objects.filter(owner=request.user)}
        if url_re.fullmatch(url) is not None:
            shortlink = secrets.token_urlsafe(10)[:7] if shortlink == "" else shortlink
            if Link.objects.filter(shortlink=shortlink).first() is not None:
                context["error"] = "shortlink already exists"
            else:
                link = Link(url=url, shortlink=shortlink, owner=request.user)
                link.save()
        else:
            context["error"] = "url invalid"
        
        return render(request, "linker/link_list.html", context=context)

@login_required
def delete_link(request, id):
    user:User = request.user
    link = Link.objects.get(pk=id)
    if link is not None:
        if request.user == link.owner:
            link.delete()
        elif user.is_superuser:
            link.delete()
        else:
            print("no action")
    return redirect('links')

def oauth_callback(request):
    code = request.GET.get("code")
    if code is not None:
        params = {
            "client_id": "secret",
            "code": code,
            "client_secret":"secret",
            "redirect_uri":"http://localhost:8000/login/oauth_callback",
        }
        headers= {
            "Accept":"application/json"
        }
        res = requests.post("https://github.com/login/oauth/access_token",   
                            params=params, headers=headers)
        token = res.json().get("access_token","")
        res = requests.get("https://api.github.com/user", 
            headers={"Authorization": f"token {token}"})
        
        data = {k: v for k, v in res.json().items() if k in ["login","id","avatar_url","name","email"]}
        user = User.objects.filter(username=data.get("login")).first()

        if user is not None:
            # kalau udah ada, authenticate
            login(request, user)
        else:
            # kalau gk ada bikin user baru
            user = User(username=data.get("login"), is_superuser=False, first_name=data.get("name",""))
            user.save()
            login(request, user)
        
    return redirect("/")

def logout_fn(request):
    logout(request)
    return redirect("/")