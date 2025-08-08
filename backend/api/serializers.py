from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import (Type, Status, Category, Subcategory, Operation)


class StatusSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    class Meta:
        model = Status
        fields = ['id', 'name']

    def validate_name(self, value):
        qs = Status.objects.filter(name=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("Статус с таким именем уже существует")
        return value


class TypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    class Meta:
        model = Type
        fields = ['id', 'name']
    
    def validate_name(self, value):
        qs = Type.objects.filter(name=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("Тип с таким именем уже существует")
        return value


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    type = serializers.PrimaryKeyRelatedField(queryset=Type.objects.all())

    class Meta:
        model = Category
        fields = ['id', 'name', 'type']

    def validate(self, data):
        qs = Category.objects.filter(name=data['name'], type=data['type'])
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("Категория с таким именем уже существует для данного типа")
        return data


class SubcategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'category']

    def validate(self, data):
        qs = Subcategory.objects.filter(name=data['name'], category=data['category'])
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("Подкатегория с таким именем уже существует для данной категории")
        return data


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ['id', 'date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment']

    def validate(self, data):
        if data['category'].type_id != data['type'].id:
            raise ValidationError("Выбранная категория не принадлежит выбранному типу")
        if data['subcategory'].category_id != data['category'].id:
            raise ValidationError("Выбранная подкатегория не принадлежит выбранной категории")
        if data['amount'] < 0:
            raise ValidationError("Сумма не может быть отрицательной")
        return data