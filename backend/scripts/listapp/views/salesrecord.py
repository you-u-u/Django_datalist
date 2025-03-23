from django.shortcuts import render
from .models import SalesRecord  # 既存のモデルを使用

def salesrecord_list(request):
    filters = {}

    if request.GET.get("start_month") and request.GET.get("end_month"):
        filters["order_date__year__gte"], filters["order_date__month__gte"] = map(int, request.GET["start_month"].split("-"))
        filters["order_date__year__lte"], filters["order_date__month__lte"] = map(int, request.GET["end_month"].split("-"))

    if request.GET.get("customer_id"):
        filters["customer_id"] = request.GET["customer_id"]

    data = SalesRecord.objects.filter(**filters)
    return render(request, "salesrecord/list.html", {"data": data})

