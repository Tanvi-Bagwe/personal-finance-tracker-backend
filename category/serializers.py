from rest_framework import serializers
from .models import Category
from category.constant import CategoryFields

class CreateCategorySerializer(serializers.Serializer):

    name = serializers.CharField(max_length=100)

    type = serializers.ChoiceField(
        choices=[CategoryFields.INCOME, CategoryFields.EXPENSE]
    )

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category

        fields = [
            CategoryFields.ID,
            CategoryFields.NAME,
            CategoryFields.TYPE
        ]