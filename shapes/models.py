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
    regex=r'^#(?:[0-9a-fA-F]{3}){1,2}$',
    message='Enter a valid hex color code (e.g., #FFFFFF).'
)

class ShapeType(models.TextChoices):
    CIRCLE = 'circle', 'Circle'
    SQUARE = 'square', 'Square'
    TRIANGLE = 'triangle', 'Triangle'

class Shape(models.Model):
    name = models.CharField(max_length=50, validators=[name_validator])
    shape = models.CharField(max_length=20, choices=ShapeType.choices, db_column="shape_type", validators=[shape_validator])
    color = models.CharField(max_length=7, db_column="shape_color", validators=[hex_color_validator])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        db_table = "shapes"
        verbose_name = "Shape"
        verbose_name_plural = "Shapes"