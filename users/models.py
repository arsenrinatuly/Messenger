from django.db import models
<<<<<<< HEAD

# Create your models here.
=======
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Codes(models.Model):
    code = models.CharField(
        unique=False,
        default="qwertyuiop",
        verbose_name="код активации"
    )
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name="code"
    )
    created_at = models.DateTimeField(
        verbose_name="Срок действия",
        default=timezone.now
    )
>>>>>>> d211408 (hz)
