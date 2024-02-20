from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save


class Genre(models.Model):
    name=models.CharField(max_length=200,unique=True)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now_add=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
       return self.name
    
class Language(models.Model):
    name=models.CharField(max_length=200,unique=True)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now_add=True)
    is_active=models.BooleanField(default=True)


class Movie(models.Model):
    title=models.CharField(max_length=200,)
    released_at=models.PositiveIntegerField()
    genre=models.ManyToManyField(Genre,related_name="gen")
    language=models.ManyToManyField(Language,related_name="lang")
    poster=models.ImageField(upload_to="image",default="default.jpg",blank=True)
    directed_by=models.CharField(max_length=200)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now_add=True)
    is_active=models.BooleanField(default=True)

class Review(models.Model):
    reviewer=models.ForeignKey(User,on_delete=models.CASCADE,related_name="critic")
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE, related_name="r_movie",)
    text=models.CharField(max_length=200,blank=True)
    rating=models.PositiveBigIntegerField(blank=True,validators=[MinValueValidator(1),MaxValueValidator(5)] )
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now_add=True)
    is_active=models.BooleanField(default=True)



class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    user_name=models.CharField(max_length=200)
    user_profile=models.ImageField(upload_to="profileimages", default="profile.jpg")
    dob=models.DateField()
    options=(("male","male")),(("female","female"))
    gender=models.CharField(max_length=200,choices=options)
    watchlist=models.ManyToManyField(Movie,blank=True,null=True, related_name="wlm")
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now_add=True)
    is_active=models.BooleanField(default=True)


def valid_user(sender,instance,created,**kwargs):
    if created and not instance.is_superuser:
        UserProfile.objects.create(user=instance)

post_save.connect(valid_user,sender=User)

