from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Community

def home(request): return render(request,"home.html")
def feed(request):
    return render(request,"feed.html",{"posts":Post.objects.all().order_by("-created_at")})
@login_required
def create_post(request):
    if request.method=="POST":
        Post.objects.create(
            author=request.user,
            title=request.POST["title"],
            body=request.POST["body"],
            code=request.POST.get("code",""),
            code_language=request.POST.get("code_language",""),
        )
        return redirect("feed")
    return render(request,"create_post.html")
def post_detail(request,pk):
    return render(request,"post_detail.html",{"post":get_object_or_404(Post,pk=pk)})
def communities(request):
    return render(request,"communities.html",{"communities":Community.objects.all()})
def inbox(request): return render(request,"inbox.html")
