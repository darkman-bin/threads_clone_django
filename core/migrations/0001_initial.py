from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("display_name", models.CharField(blank=True, max_length=60)),
                ("bio", models.CharField(blank=True, max_length=160)),
                ("avatar", models.ImageField(blank=True, null=True, upload_to="avatars/")),
                ("following", models.ManyToManyField(blank=True, related_name="followers", to=settings.AUTH_USER_MODEL)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="profile", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Thread",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("content", models.TextField(validators=[django.core.validators.MaxLengthValidator(500)])),
                ("image", models.ImageField(blank=True, null=True, upload_to="threads/")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("author", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="threads", to=settings.AUTH_USER_MODEL)),
                ("likes", models.ManyToManyField(blank=True, related_name="liked_threads", to=settings.AUTH_USER_MODEL)),
                ("parent", models.ForeignKey(blank=True, help_text="لو كان هذا المنشور ردّاً على منشور آخر", null=True, on_delete=django.db.models.deletion.CASCADE, related_name="replies", to="core.thread")),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
