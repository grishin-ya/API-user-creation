from django.contrib.auth.models import AbstractUser
from django.db import models

class Direction(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ("HR", "HR"),
        ("MENTOR", "Mentor"),
        ("HEAD", "Head"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='HR')
    is_admin = models.BooleanField(default=False)
    directions = models.ManyToManyField(
        Direction,
        blank=True,
        related_name="users"
    )

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.is_admin = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"


class Trainee(models.Model):
    STATUS_CHOICES = [
        ('INTERNSHIP', 'Internship'),
        ('JUNIOR', 'Junior'),
        ('MIDDLE', 'Middle'),
        ('REJECTED', 'Rejected'),
    ]

    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='INTERNSHIP')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    rejection_reason = models.TextField(null=True, blank=True)
    mentor = models.ForeignKey(
        CustomUser,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='trainees'
    )
    directions = models.ManyToManyField(Direction, related_name='trainees')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
