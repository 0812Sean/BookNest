from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Book(models.Model):
    CATEGORY_CHOICES = [
        ('Mystery', 'Mystery'),
        ('Thriller', 'Thriller'),
        ('Science Fiction', 'Science Fiction'),
        ('Romance', 'Romance'),
        ('Fantasy', 'Fantasy'),
        ('Classic', 'Classic'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=200)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='cover_images/', max_length=555, blank=True, null=True) 
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)]) 
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    favorited_by = models.ManyToManyField(User, related_name='favorite_books', blank=True)

    def __str__(self):
        return f"{self.title} by {self.author} - {self.user.username}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.book.title}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    background_color = models.CharField(max_length=7, default="#ffffff")

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
