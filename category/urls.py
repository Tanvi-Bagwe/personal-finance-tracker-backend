from django.urls import path

from category.views import ListCategoriesView, CreateCategoryView, UpdateCategoryView, DeleteCategoryView

urlpatterns = [

    path("", ListCategoriesView.as_view()),
    path("create", CreateCategoryView.as_view()),
    path("<int:category_id>/update", UpdateCategoryView.as_view()),
    path("<int:category_id>/delete", DeleteCategoryView.as_view()),
]