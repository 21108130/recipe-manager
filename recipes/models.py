from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    """Recipe categories like Breakfast, Lunch, Dinner"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Recipe(models.Model):
    """Main Recipe model"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.TextField(help_text="List ingredients separated by commas")
    instructions = models.TextField()
    preparation_time = models.IntegerField(help_text="Time in minutes")
    cooking_time = models.IntegerField(help_text="Time in minutes")
    servings = models.IntegerField(default=4)

    # Image upload
    image = models.ImageField(upload_to='recipe_pics/', blank=True, null=True)

    # Relationships
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')

    # Timestamps
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    # Features
    likes = models.ManyToManyField(User, related_name='liked_recipes', blank=True)

    def __str__(self):
        return self.title

    @property
    def total_likes(self):
        return self.likes.count()

    class Meta:
        ordering = ['-created_date']

class Profile(models.Model):
    """Extended user profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default.jpg', blank=True)
    location = models.CharField(max_length=100, blank=True)
    favorite_food = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'