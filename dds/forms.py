from django import forms
from .models import Status, TransactionType, Category, SubCategory, Transaction


class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ["date", "status", "transaction_type", "category", "subcategory", "amount", "comment"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "transaction_type": forms.Select(attrs={"class": "form-control", "id": "id_transaction_type"}),
            "category": forms.Select(attrs={"class": "form-control", "id": "id_category"}),
            "subcategory": forms.Select(attrs={"class": "form-control", "id": "id_subcategory"}),
            "amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            # При редактировании отображаем только связанные категории и подкатегории
            self.fields["category"].queryset = Category.objects.filter(
                transaction_type=self.instance.transaction_type
            )
            self.fields["subcategory"].queryset = SubCategory.objects.filter(
                category=self.instance.category
            )
        else:
            # При создании записи отображаем все категории и подкатегории
            self.fields["category"].queryset = Category.objects.all()
            self.fields["subcategory"].queryset = SubCategory.objects.all()

        self.fields["comment"].required = False


    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get("transaction_type")
        category = cleaned_data.get("category")
        subcategory = cleaned_data.get("subcategory")

        if category and transaction_type:
            if category.transaction_type != transaction_type:
                self.add_error("category", "Категория не относится к выбранному типу")

        if subcategory and category:
            if subcategory.category != category:
                self.add_error("subcategory", "Подкатегория не относится к выбранной категории")

        return cleaned_data