from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class Like(models.Model):
    like = models.BooleanField()
    created = models.DateTimeField()
    reviewid = models.ForeignKey('Review', models.DO_NOTHING)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + " | " + str(self.user) + " | " + str(self.reviewid.restid)

class Region(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('region-detail', args=[str(self.id)])

class Restaurant(models.Model):
    restname = models.CharField(max_length=200)
    phone = models.IntegerField()
    address = models.CharField(max_length=200)
    cuisine = models.CharField(max_length=200)
    regionid = models.ForeignKey('Region', models.DO_NOTHING)
    last_modify_date = models.DateTimeField()
    created = models.DateTimeField()

    def __str__(self):
        return self.restname

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('rest-detail', args=[str(self.id)])

class Review(models.Model):
    overallRating = models.PositiveIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])  # Field name made lowercase. max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    price = models.DecimalField(max_digits=10, decimal_places=1)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    comment = models.TextField()
    dateofvisit = models.DateField(verbose_name= 'Date of Visit (YYYY-MM-DD)')  # Field name made lowercase.
    created = models.DateTimeField(auto_now=True)
    restid = models.ForeignKey('Restaurant', models.DO_NOTHING, verbose_name= 'Restaurant')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank= True, related_name='post_likes')

    def get_absolute_url(self):
        return reverse('review-create', args=[str(self.restid.id)])

    class Meta:
        permissions = (("all_review","Read all reviews"),)

class ReviewInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    review = models.ForeignKey('Review', on_delete=models.SET_NULL, null=True)
    comment = models.TextField()
    created = models.DateTimeField(auto_now=True)
    restid = models.ForeignKey('Restaurant', models.DO_NOTHING, verbose_name= 'Restaurant')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return '{0} ({1})'.format(self.id, self.review.restid)


