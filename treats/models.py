import datetime

from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Treat(models.Model):
    """A baked good the user has made before or plans to make."""

    class Ratings(models.TextChoices):
        ONE_STAR = 1, '⭐'
        TWO_STARS = 2, '⭐⭐'
        THREE_STARS = 3, '⭐⭐⭐'
        FOUR_STARS = 4, '⭐⭐⭐⭐'
        FIVE_STARS = 5, '⭐⭐⭐⭐⭐'

    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    slug = models.SlugField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cover_img = models.URLField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    rating = models.CharField(max_length=1, choices=Ratings.choices,
                              default=Ratings.THREE_STARS)
    recipe_source = models.TextField(max_length=250, blank=True)

    class Meta:
        ordering = ['rating', 'created']
        indexes = [
            models.Index(fields=['-rating']),
            models.Index(fields=['created'])
        ]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Treat, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Note(models.Model):
    """Details about a Treat, treat recipe, or other aspect of a treat."""
    treat = models.ForeignKey(Treat, on_delete=models.CASCADE, related_name='notes')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]

    def __str__(self):
        return f'Note on {self.treat}: {self.body[:20]}...'


class Coupon(models.Model):
    """
    A voucher for one baked good. The baker user assigns coupons to the recipient user.
    The coupon includes info like:
        --Upon creation by baker user--
        the purpose of the coupon (birthday, promotion, appreciation, won a bet)
        person/user associated with coupon
        assignment date: automatic upon creation
        event date: not required
        expiration date: required, manually selected
        --Upon receipt by recipient--
        treat selected: in catalogue or not in catalogue
    """

    class Status(models.TextChoices):
        NOT_SENT_YET = 'Not sent yet'
        WAITING_FOR_RESPONSE = 'Waiting for response'
        TO_DO = 'To Do'
        IN_PROGRESS = 'In Progress'
        DONE = 'Done'
        EXPIRED = 'Expired'

    reason = models.CharField(max_length=50)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE,
                                  null=True, blank=True)
    # maybe a way to have placeholder user would be nice

    # gets written when coupon is redeemed
    treat = models.ForeignKey(Treat, on_delete=models.SET_NULL,
                              null=True, blank=True)

    # if baker is filling out, they can select from catalogue, otherwise leave empty for recipient to fill out

    created = models.DateTimeField(auto_now_add=True)

    # i.e. the birthday, 1st day of promotion, etc
    target_date = models.DateTimeField(default=timezone.now)

    # for coupons that "never expire" -> +100 years or something similar
    expiration_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NOT_SENT_YET)

    @property
    def is_redeemed(self):
        return self.treat is not None

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]

    def __str__(self):
        return (
            f'For {self.reason.lower()} on '
            f'{self.target_date.strftime("%m/%d/%y")} | Expires'
            f' on {self.expiration_date.strftime("%m/%d/%y")}.'
        )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_baker_user = models.BooleanField(default=False)

    def __str__(self):
        if self.is_baker_user:
            return f'User {self.user.username}: Baker User'
        else:
            return f'User {self.user.username}: NOT a Baker User'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# class Comment(models.Model):
#     treat = models.ForeignKey(Treat, on_delete=models.CASCADE)
#     body = models.TextField()
#     publish = models.DateTimeField(default=timezone.now)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#
#
# class Review(models.Model):
#     treat = models.ForeignKey(Treat, on_delete=models.CASCADE)
#     body = models.TextField()
#     rating = models.IntegerField()
#     publish = models.DateTimeField(default=timezone.now)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
