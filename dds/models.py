from django.db import models


from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Status(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Статус"
    )

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        ordering = ["name"]

    def __str__(self):
        return self.name


class TransactionType(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Тип"
    )

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Категория"
    )

    transaction_type = models.ForeignKey(
        TransactionType,
        on_delete=models.CASCADE,
        related_name="categories",
        verbose_name="Тип"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

        constraints = [
            models.UniqueConstraint(
                fields=["name", "transaction_type"],
                name="unique_category_per_type"
            )
        ]

        ordering = ["name"]

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Подкатегория"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="subcategories",
        verbose_name="Категория"
    )

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"

        constraints = [
            models.UniqueConstraint(
                fields=["name", "category"],
                name="unique_subcategory_per_category"
            )
        ]

        ordering = ["name"]

    def __str__(self):
        return self.name


class Transaction(models.Model):
    date = models.DateField(
        default=timezone.now,
        verbose_name="Дата"
    )

    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name="Статус"
    )

    transaction_type = models.ForeignKey(
        TransactionType,
        on_delete=models.PROTECT,
        verbose_name="Тип"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name="Категория"
    )

    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.PROTECT,
        verbose_name="Подкатегория"
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Сумма"
    )

    comment = models.TextField(
        blank=True,
        verbose_name="Комментарий"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создано"
    )

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"

        ordering = ["-date"]

        indexes = [
            models.Index(fields=["date"]),
            models.Index(fields=["status"]),
            models.Index(fields=["transaction_type"]),
        ]

    def clean(self):
        errors = {}

        if self.amount is not None and self.amount <= 0:
            errors["amount"] = (
                "Сумма должна быть больше нуля"
            )

        if (
            self.category
            and self.transaction_type
            and self.category.transaction_type != self.transaction_type
        ):
            errors["category"] = (
                "Категория не относится к выбранному типу"
            )

        if (
            self.subcategory
            and self.category
            and self.subcategory.category != self.category
        ):
            errors["subcategory"] = (
                "Подкатегория не относится к выбранной категории"
            )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.date} | "
            f"{self.transaction_type} | "
            f"{self.amount} ₽"
        )