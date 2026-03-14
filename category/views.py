from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .constant import CategoryFields
from .models import Category
from .serializers import CreateCategorySerializer, CategorySerializer


class CreateCategoryView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = CreateCategorySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        name = serializer.validated_data[CategoryFields.NAME]
        category_type = serializer.validated_data[CategoryFields.TYPE]

        category = Category.objects.create(
            user=request.user,
            name=name,
            type=category_type
        )

        return Response({
            "message": "Category created",
            "id": category.id
        })

class ListCategoriesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.filter(user=request.user)

        serializer = CategorySerializer(categories, many=True)

        return Response(serializer.data)


class UpdateCategoryView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, category_id):

        try:
            category = Category.objects.get(
                id=category_id,
                user=request.user
            )

        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=404)

        serializer = CreateCategorySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        category.name = serializer.validated_data[CategoryFields.NAME]
        category.type = serializer.validated_data[CategoryFields.TYPE]

        category.save()

        return Response({"message": "Category updated"})


class DeleteCategoryView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, category_id):

        try:
            category = Category.objects.get(
                id=category_id,
                user=request.user
            )

        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=404)

        category.delete()

        return Response({"message": "Category deleted"})