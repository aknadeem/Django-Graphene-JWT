from django.db import models

# Create your models here.

class User(models.Model):
    user_name = models.CharField(max_length=100)
    email = models.EmailField(blank=False, max_length=254)
    password = models.CharField(max_length=100)
    user_level = models.CharField(max_length=100)

    def __str__(self):
        return self.user_name

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    notes = models.TextField()
    category = models.ForeignKey(
        Category, related_name="ingredients", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name