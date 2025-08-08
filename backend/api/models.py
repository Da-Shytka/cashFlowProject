from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name


class Category(models.Model):    
    name = models.CharField(max_length=50)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='categories')
    class Meta:
        unique_together = ('type', 'name')
    def __str__(self):
        return f"{self.name} ({self.type.name})"


class Subcategory(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    class Meta:
        unique_together = ('name', 'category')
    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Operation(models.Model):
    date = models.DateField(auto_now_add=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.date} - {self.amount}₽"