from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_prices.models import PriceField
from phonenumber_field.modelfields import PhoneNumberField


class Author(models.Model):
    name = models.CharField(max_length=120)
    surname = models.CharField(max_length=120, blank=True)
    photo = models.ImageField(upload_to='author')  # TODO: store images in Amazon S3

    def __str__(self):
        return f'{self.name} {self.surname}'


class Book(models.Model):
    authors = models.ManyToManyField(Author, related_name='books')
    photo = models.ImageField(upload_to='book', null=True, blank=True)  # TODO: store images in Amazon S3
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = PriceField('Price', currency='BTC', max_digits=12, decimal_places=2)
    link = models.URLField()

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = PhoneNumberField()
    bought_books = models.ManyToManyField(Book, blank=True, related_name='buyers')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Card(models.Model):
    owner = models.ForeignKey(Profile, related_name='cards', on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    # TODO: do not store sensitive data non-crypted
    payment_number = models.CharField(max_length=19, validators=(MinLengthValidator(12),))

    def __str__(self):
        return str(self.name)

