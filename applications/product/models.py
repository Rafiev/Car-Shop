from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

User = get_user_model()


class Car(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')
    CAR_CATEGORY_CHOICES = [('A', 'Motorbike'), ('B', 'Automobile'), ('C', 'Truck'), ('D', 'Bus')]
    category = models.CharField(max_length=1, choices=CAR_CATEGORY_CHOICES)
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='comments', null=True)
    post = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.owner}: {self.post.title}'


class Like(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='likes')
    like = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.owner}: {self.like}'


class Rating(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    post = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='ratings')
    rating = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True, null=True)

    def __str__(self):
        return f'{self.owner}: {self.rating}'


class Image(models.Model):
    post = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')


class Sale(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order')
    post = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='status')
    status = models.BooleanField(default=False)


class Save(models.Model):
    post = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='saves')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saves')
    save_status = models.BooleanField(default=False)