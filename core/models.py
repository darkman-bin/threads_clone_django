from django.conf import settings
from django.db import models
from django.core.validators import MaxLengthValidator

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    display_name = models.CharField(max_length=60, blank=True)
    bio = models.CharField(max_length=160, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    # المستخدمون الذين أتابعهم
    following = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="followers",
        blank=True,
    )

    def __str__(self):
        return f"@{self.user.username}"

    @property
    def followers_count(self):
        return self.user.followers.count()

    @property
    def following_count(self):
        return self.following.count()


class Thread(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="threads")
    content = models.TextField(validators=[MaxLengthValidator(500)])
    image = models.ImageField(upload_to="threads/", blank=True, null=True)

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="replies",
        blank=True,
        null=True,
        help_text="لو كان هذا المنشور ردّاً على منشور آخر",
    )

    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_threads", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Thread({self.id}) by @{self.author.username}"

    @property
    def is_reply(self):
        return self.parent_id is not None

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def replies_count(self):
        return self.replies.count()
