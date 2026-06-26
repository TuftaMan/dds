from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Status, TransactionType, Category, SubCategory, Transaction
from .forms import TransactionForm
from django.contrib import messages
from django.db.models import ProtectedError


def transaction_list(request):
    transactions = Transaction.objects.select_related(
        "status", "transaction_type", "category", "subcategory"
    )

    # Фильтры
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")
    status_id = request.GET.get("status")
    type_id = request.GET.get("transaction_type")
    category_id = request.GET.get("category")
    subcategory_id = request.GET.get("subcategory")

    if date_from:
        transactions = transactions.filter(date__gte=date_from)
    if date_to:
        transactions = transactions.filter(date__lte=date_to)
    if status_id:
        transactions = transactions.filter(status_id=status_id)
    if type_id:
        transactions = transactions.filter(transaction_type_id=type_id)
    if category_id:
        transactions = transactions.filter(category_id=category_id)
    if subcategory_id:
        transactions = transactions.filter(subcategory_id=subcategory_id)

    context = {
        "transactions": transactions,
        "statuses": Status.objects.all(),
        "types": TransactionType.objects.all(),
        "categories": Category.objects.all(),
        "subcategories": SubCategory.objects.all(),
        # для сохранения значений фильтров
        "filters": {
            "date_from": date_from or "",
            "date_to": date_to or "",
            "status": status_id or "",
            "transaction_type": type_id or "",
            "category": category_id or "",
            "subcategory": subcategory_id or "",
        }
    }
    return render(request, "dds/transaction_list.html", context)

# Создание новой транзакции
def transaction_create(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dds:transaction_list")
    else:
        form = TransactionForm()

    context = {
        "form": form,
        "title": "Создать запись",
    }
    return render(request, "dds/transaction_form.html", context)

# Изменение транзакции
def transaction_edit(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect("dds:transaction_list")
    else:
        form = TransactionForm(instance=transaction)

    context = {
        "form": form,
        "title": "Редактировать запись",
        "transaction": transaction,
    }
    return render(request, "dds/transaction_form.html", context)

# Удаление
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == "POST":
        transaction.delete()
        return redirect("dds:transaction_list")

    context = {
        "transaction": transaction,
    }
    return render(request, "dds/transaction_confirm_delete.html", context)


# AJAX для динамической фильтрации категорий и подкатегорий
def get_categories(request):
    type_id = request.GET.get("type_id")
    categories = Category.objects.filter(transaction_type_id=type_id).values("id", "name")
    return JsonResponse(list(categories), safe=False)


def get_subcategories(request):
    category_id = request.GET.get("category_id")
    subcategories = SubCategory.objects.filter(category_id=category_id).values("id", "name")
    return JsonResponse(list(subcategories), safe=False)

# Справочники

def references(request):
    context = {
        "statuses": Status.objects.all(),
        "types": TransactionType.objects.all(),
        "categories": Category.objects.all(),
        "subcategories": SubCategory.objects.all(),
    }
    return render(request, "dds/references.html", context)


# Статусы
def status_create(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        if name:
            Status.objects.create(name=name)
            messages.success(request, f"Статус «{name}» добавлен")
    return redirect("dds:references")


def status_edit(request, pk):
    status = get_object_or_404(Status, pk=pk)
    if request.method == "POST":
        form_name = request.POST.get("name", "").strip()
        if form_name:
            status.name = form_name
            status.save()
            messages.success(request, f"Статус обновлён")
        return redirect("dds:references")

    context = {"object": status, "title": "Редактировать статус", "back_url": "dds:references"}
    return render(request, "dds/reference_form.html", context)


def status_delete(request, pk):
    status = get_object_or_404(Status, pk=pk)
    if request.method == "POST":
        status.delete()
        messages.success(request, "Статус удалён")
        return redirect("dds:references")

    context = {"object": status, "title": "Удалить статус", "back_url": "dds:references"}
    return render(request, "dds/reference_confirm_delete.html", context)


# Типы
def type_create(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        if name:
            TransactionType.objects.create(name=name)
            messages.success(request, f"Тип «{name}» добавлен")
    return redirect("dds:references")


def type_edit(request, pk):
    transaction_type = get_object_or_404(TransactionType, pk=pk)
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        if name:
            transaction_type.name = name
            transaction_type.save()
            messages.success(request, "Тип обновлён")
        return redirect("dds:references")

    context = {"object": transaction_type, "title": "Редактировать тип", "back_url": "dds:references"}
    return render(request, "dds/reference_form.html", context)


def type_delete(request, pk):
    transaction_type = get_object_or_404(TransactionType, pk=pk)
    if request.method == "POST":
        transaction_type.delete()
        messages.success(request, "Тип удалён")
        return redirect("dds:references")

    context = {"object": transaction_type, "title": "Удалить тип", "back_url": "dds:references"}
    return render(request, "dds/reference_confirm_delete.html", context)


# Категории
def category_create(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        type_id = request.POST.get("transaction_type")
        if name and type_id:
            transaction_type = get_object_or_404(TransactionType, pk=type_id)
            Category.objects.create(name=name, transaction_type=transaction_type)
            messages.success(request, f"Категория «{name}» добавлена")
    return redirect("dds:references")


def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        type_id = request.POST.get("transaction_type")
        if name and type_id:
            category.name = name
            category.transaction_type = get_object_or_404(TransactionType, pk=type_id)
            category.save()
            messages.success(request, "Категория обновлена")
        return redirect("dds:references")

    context = {
        "object": category,
        "title": "Редактировать категорию",
        "types": TransactionType.objects.all(),
        "selected_type_id": category.transaction_type_id,
    }
    return render(request, "dds/category_form.html", context)


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Категория удалена")
        return redirect("dds:references")

    context = {"object": category, "title": "Удалить категорию"}
    return render(request, "dds/reference_confirm_delete.html", context)


# Подкатегории
def subcategory_create(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        category_id = request.POST.get("category")
        if name and category_id:
            category = get_object_or_404(Category, pk=category_id)
            SubCategory.objects.create(name=name, category=category)
            messages.success(request, f"Подкатегория «{name}» добавлена")
    return redirect("dds:references")


def subcategory_edit(request, pk):
    subcategory = get_object_or_404(SubCategory, pk=pk)
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        category_id = request.POST.get("category")
        if name and category_id:
            subcategory.name = name
            subcategory.category = get_object_or_404(Category, pk=category_id)
            subcategory.save()
            messages.success(request, "Подкатегория обновлена")
        return redirect("dds:references")

    context = {
        "object": subcategory,
        "title": "Редактировать подкатегорию",
        "categories": Category.objects.select_related("transaction_type").all(),
        "selected_category_id": subcategory.category_id,
    }
    return render(request, "dds/subcategory_form.html", context)


def subcategory_delete(request, pk):
    subcategory = get_object_or_404(SubCategory, pk=pk)

    if request.method == "POST":
        try:
            subcategory.delete()
            messages.success(request, "Подкатегория удалена")
        except ProtectedError:
            messages.error(
                request,
                "Нельзя удалить подкатегорию, так как она используется в транзакциях."
            )

        return redirect("dds:references")

    context = {
        "object": subcategory,
        "title": "Удалить подкатегорию",
    }

    return render(request, "dds/reference_confirm_delete.html", context)