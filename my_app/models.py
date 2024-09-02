from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    CATEGORY_CHOICES = [
        ('Mystery', 'Mystery'),
        ('Thriller', 'Thriller'),
        ('Science Fiction', 'Science Fiction'),
        ('Romance', 'Romance'),
        ('Fantasy', 'Fantasy'),
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
