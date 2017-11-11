from django.db import models
from future.utils import python_2_unicode_compatible


@python_2_unicode_compatible
class UserInformation(models.Model):
    class Meta:
        verbose_name = "کاربران تلگرام بات"
        verbose_name_plural = "کاربران تلگرام بات"

    user_id = models.CharField(max_length=20, verbose_name="کد کاربری تلگرام", unique=True)
    username = models.CharField(max_length=100, verbose_name="نام انتخابی کاربر", default="ندارد")
    first_name = models.CharField(max_length=100, verbose_name="نام کاربر", default="ندارد")
    last_name = models.CharField(max_length=100, verbose_name="فامیل کاربر", default="ندارد")
    phone_number = models.CharField(max_length=100, verbose_name="شماره تلفن", default="ندارد")
    createdTime = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")
    changedTime = models.DateTimeField(auto_now=True, verbose_name="آخرین تغییر")
    rate = models.CharField(max_length=10, verbose_name="امتیاز", default="0")
    start = models.CharField(max_length=10, verbose_name="شروع مسابقه", default="شروع نکرده")

    def __str__(self):
        return str(self.user_id)
