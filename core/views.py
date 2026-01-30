from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator

from .forms import RegisterForm, ThreadForm, ProfileForm, LoginForm
from .models import Thread, Profile

User = get_user_model()



def _ensure_profile(user):
    # أمان إضافي في حال كان هناك مستخدم قديم بدون Profile
    Profile.objects.get_or_create(user=user, defaults={"display_name": user.username})


def home(request):
    if request.user.is_authenticated:
        return redirect("feed")
    return render(request, "landing.html")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("feed")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            _ensure_profile(user)
            # profile يُنشأ تلقائياً عبر signals
            messages.success(request, "تم إنشاء الحساب بنجاح ✅ تفضل سجّل دخولك.")
            return redirect("login")
        else:
            messages.error(request, "تأكد من البيانات وحاول مرة ثانية.")
    else:
        form = RegisterForm()

    return render(request, "auth/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("feed")

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "هلا! تم تسجيل الدخول ✅")
            return redirect("feed")
        else:
            messages.error(request, "اسم المستخدم أو كلمة المرور غير صحيحة.")
    else:
        form = LoginForm()

    return render(request, "auth/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "تم تسجيل الخروج.")
    return redirect("home")


@login_required
def feed(request):
    _ensure_profile(request.user)
    # نشر ثريد جديد
    if request.method == "POST":
        form = ThreadForm(request.POST, request.FILES)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.save()
            messages.success(request, "تم نشر الثريد ✅")
            return redirect("feed")
        else:
            messages.error(request, "تعذر نشر الثريد. تحقق من المحتوى.")
    else:
        form = ThreadForm()

    following_users = list(request.user.profile.following.all())
    timeline_users = following_users + [request.user]

    qs = (
        Thread.objects
        .filter(parent__isnull=True, author__in=timeline_users)
        .select_related("author", "author__profile")
        .prefetch_related("likes")
    )

    paginator = Paginator(qs, 10)
    page_number = request.GET.get("page") or 1
    page_obj = paginator.get_page(page_number)

    return render(request, "feed.html", {
        "form": form,
        "page_obj": page_obj,
    })


@login_required
def thread_detail(request, thread_id: int):
    _ensure_profile(request.user)
    thread = get_object_or_404(
        Thread.objects.select_related("author", "author__profile").prefetch_related("likes", "replies"),
        pk=thread_id
    )

    # نشر رد
    if request.method == "POST":
        form = ThreadForm(request.POST, request.FILES)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.parent = thread
            reply.save()
            messages.success(request, "تم نشر الرد ✅")
            return redirect("thread_detail", thread_id=thread.id)
        else:
            messages.error(request, "تعذر نشر الرد.")
    else:
        form = ThreadForm()

    replies = (
        thread.replies
        .select_related("author", "author__profile")
        .prefetch_related("likes")
        .order_by("created_at")
    )

    return render(request, "thread_detail.html", {
        "thread": thread,
        "replies": replies,
        "form": form,
    })


@login_required
def profile_view(request, username: str):
    _ensure_profile(request.user)
    profile_user = get_object_or_404(User, username=username)
    if not hasattr(profile_user, "profile"):
        raise Http404("Profile not found")

    threads = (
        Thread.objects
        .filter(author=profile_user, parent__isnull=True)
        .select_related("author", "author__profile")
        .prefetch_related("likes")
    )

    is_following = request.user.profile.following.filter(pk=profile_user.pk).exists() if request.user != profile_user else False

    return render(request, "profile.html", {
        "profile_user": profile_user,
        "threads": threads,
        "is_following": is_following,
    })


@login_required
def edit_profile(request):
    _ensure_profile(request.user)
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تحديث الملف الشخصي ✅")
            return redirect("profile", username=request.user.username)
        else:
            messages.error(request, "تعذر حفظ التعديلات.")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "edit_profile.html", {"form": form})


@require_POST
@login_required
def toggle_like(request, thread_id: int):
    _ensure_profile(request.user)
    thread = get_object_or_404(Thread, pk=thread_id)
    user = request.user

    if thread.likes.filter(pk=user.pk).exists():
        thread.likes.remove(user)
        liked = False
    else:
        thread.likes.add(user)
        liked = True

    return JsonResponse({
        "liked": liked,
        "likes_count": thread.likes.count(),
    })


@require_POST
@login_required
def toggle_follow(request, username: str):
    _ensure_profile(request.user)
    target = get_object_or_404(User, username=username)
    if target == request.user:
        return JsonResponse({"ok": False, "error": "لا يمكنك متابعة نفسك."}, status=400)

    prof = request.user.profile
    if prof.following.filter(pk=target.pk).exists():
        prof.following.remove(target)
        following = False
    else:
        prof.following.add(target)
        following = True

    return JsonResponse({
        "ok": True,
        "following": following,
        "followers_count": target.followers.count(),
    })
