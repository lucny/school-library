from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    profile_photo = models.ImageField(
        upload_to="users/profile_photos/%Y/%m/",
        null=True,
        blank=True,
        verbose_name="Profilová fotografie",
    )
    bio = models.TextField(blank=True, verbose_name="O mně")

class SocialLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="social_links", verbose_name="Uživatel")
    label = models.CharField(max_length=80, verbose_name="Popisek")
    url = models.URLField(max_length=500, verbose_name="URL")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Sociální odkaz"
        verbose_name_plural = "Sociální odkazy"
        ordering = ["label", "url"]

    def __str__(self) -> str:
        return f"{self.user.username}: {self.label}"
