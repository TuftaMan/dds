from django.contrib import admin
from .models import Status, TransactionType, Category, SubCategory, Transaction


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "transaction_type"]
    list_filter = ["transaction_type"]
    search_fields = ["name"]


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "get_type"]
    list_filter = ["category__transaction_type", "category"]
    search_fields = ["name"]

    def get_type(self, obj):
        return obj.category.transaction_type
    get_type.short_description = "Тип"


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["date", "status", "transaction_type", "category", "subcategory", "amount", "comment"]
    list_filter = ["status", "transaction_type", "category", "subcategory"]
    search_fields = ["comment"]
    date_hierarchy = "date"