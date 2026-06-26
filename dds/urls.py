from django.urls import path
from . import views

app_name = "dds"

urlpatterns = [
    # главная
    path("", views.transaction_list, name="transaction_list"),

    # транзакции
    path("transaction/create/", views.transaction_create, name="transaction_create"),
    path("transaction/<int:pk>/edit/", views.transaction_edit, name="transaction_edit"),
    path("transaction/<int:pk>/delete/", views.transaction_delete, name="transaction_delete"),

    # AJAX
    path("ajax/categories/", views.get_categories, name="get_categories"),
    path("ajax/subcategories/", views.get_subcategories, name="get_subcategories"),
    
    # справочники
    path("references/", views.references, name="references"),
    path("references/status/create/", views.status_create, name="status_create"),
    path("references/status/<int:pk>/edit/", views.status_edit, name="status_edit"),
    path("references/status/<int:pk>/delete/", views.status_delete, name="status_delete"),
    path("references/type/create/", views.type_create, name="type_create"),
    path("references/type/<int:pk>/edit/", views.type_edit, name="type_edit"),
    path("references/type/<int:pk>/delete/", views.type_delete, name="type_delete"),
    path("references/category/create/", views.category_create, name="category_create"),
    path("references/category/<int:pk>/edit/", views.category_edit, name="category_edit"),
    path("references/category/<int:pk>/delete/", views.category_delete, name="category_delete"),
    path("references/subcategory/create/", views.subcategory_create, name="subcategory_create"),
    path("references/subcategory/<int:pk>/edit/", views.subcategory_edit, name="subcategory_edit"),
    path("references/subcategory/<int:pk>/delete/", views.subcategory_delete, name="subcategory_delete"),
]