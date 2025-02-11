from django.db import models

# Create your models here.


class Customer(models.Model):
    created_at = models.DateField(auto_now_add=True)
    first_name = models.TextField(max_length=50)
    last_name = models.TextField(max_length=50)
    email = models.EmailField()
    phone = models.TextField(max_length=15)
    country = models.TextField(max_length=50)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
