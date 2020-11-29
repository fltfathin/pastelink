from django.db import models
from django.utils.translation import gettext_lazy as _
from django.shortcuts import reverse
from django.contrib.auth.models import User
# Create your models here.

class Link(models.Model):
    shortlink = models.CharField(_("shortlink"), max_length=50, unique=True)
    url = models.CharField(_("url"), max_length=250)
    owner = models.ForeignKey(User, verbose_name=_("link owner"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Link")
        verbose_name_plural = _("Links")

    def __str__(self):
        return f"< Link {self.shortlink} >"

    def get_absolute_url(self):
        return reverse("Link_detail", kwargs={"pk": self.pk})
