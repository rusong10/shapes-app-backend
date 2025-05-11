from django.db import models
from django.core.validators import RegexValidator

#  input validation
name_validator = RegexValidator(
    regex=r'^[A-Za-z0-9 ]+$',
    message='Name should only contain letters, numbers, and spaces.'
)

shape_validator = RegexValidator(
    regex=r'^(circle|square|triangle)$',
    message='Shape must be either "circle", "square", or "triangle".'
)

hex_color_validator = RegexValidator(
    regex=r'^#(?:[0-9a-fA-F]{3}){1,2}$',  # Match valid hex color format
    message='Enter a valid hex color code (e.g., #FFFFFF).'
)

class Shape(models.TextChoices):
    CIRCLE = 'circle', 'Circle'
    SQUARE = 'square', 'Square'
    TRIANGLE = 'triangle', 'Triangle'

class UserShape(models.Model):
    name = models.CharField(max_length=50, validators=[name_validator])
    shape = models.CharField(max_length=20, choices=Shape.choices, db_column="shape_type", validators=[shape_validator])
    color = models.CharField(max_length=7, db_column="shape_color", validators=[hex_color_validator])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        db_table = "user_shapes"
        verbose_name = " User Shape"
        verbose_name_plural = " User Shapes"
        indexes = [
            models.Index(fields=['shape']),
            models.Index(fields=['created_at']),
        ]
