from django.db import IntegrityError
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.constants import ResponseMessages, ResponseFields
from .constant import CategoryFields
from .models import Category
from .serializers import CreateCategorySerializer, CategorySerializer


class CreateCategoryView(APIView):
    """Create a new category"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateCategorySerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        name = serializer.validated_data[CategoryFields.NAME]
        category_type = serializer.validated_data[CategoryFields.TYPE]

        # Check if category with same name already exists
        if Category.objects.filter(user=request.user, name__iexact=name).exists():
            raise ValidationError(ResponseMessages.CATEGORY_EXISTS)

        try:
            category = Category.objects.create(
                user=request.user,
                name=name,
                type=category_type
            )
            return Response({
                ResponseFields.MESSAGE: ResponseMessages.CATEGORY_RECORDED,
                CategoryFields.ID: category.id
            })

        except IntegrityError:
            raise ValidationError(ResponseMessages.CATEGORY_EXISTS)


class ListCategoriesView(APIView):
    """Get all categories for the user"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.filter(user=request.user)

        serializer = CategorySerializer(categories, many=True)

        return Response(serializer.data)


class UpdateCategoryView(APIView):
    """Update an existing category"""

    permission_classes = [IsAuthenticated]

    def put(self, request, category_id):

        try:
            category = Category.objects.get(
                id=category_id,
                user=request.user
            )

        except Category.DoesNotExist:
            raise NotFound(ResponseMessages.CATEGORY_NOT_FOUND)

        serializer = CreateCategorySerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        category.name = serializer.validated_data[CategoryFields.NAME]
        category.type = serializer.validated_data[CategoryFields.TYPE]

        category.save()

        return Response({ResponseFields.MESSAGE: ResponseMessages.CATEGORY_UPDATED})


class DeleteCategoryView(APIView):
    """Delete a category"""

    permission_classes = [IsAuthenticated]

    def delete(self, request, category_id):

        try:
            category = Category.objects.get(
                id=category_id,
                user=request.user
            )

        except Category.DoesNotExist:
            raise NotFound(ResponseMessages.CATEGORY_NOT_FOUND)

        category.delete()

        return Response({ResponseFields.MESSAGE: ResponseMessages.CATEGORY_DELETED})
