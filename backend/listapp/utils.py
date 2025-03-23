# from django.apps import apps
# from django.db.models import Sum
# from collections import defaultdict
# import pandas as pd

# def fetch_sales_data(request, model_name, date_field, agg_field):
#     """ 汎用的な売上データ取得・集計処理 """
#     from .forms import SalesFilterForm

#     form = SalesFilterForm(request.GET)

#     if not form.is_valid():
#         return {"form": form}  # フォームが無効ならそのまま返す

#     period = form.cleaned_data["period"]
#     start_date = form.cleaned_data["start_date"]
#     end_date = form.cleaned_data["end_date"]
#     category = form.cleaned_data["category"]
#     keyword = form.cleaned_data["keyword"]

#     model = apps.get_model("listapp", model_name)

#     # 日次 / 月次 の切り替え
#     if period == "month":
#         date_format = "%Y/%m"
#         date_fields = [f"{date_field}__year", f"{date_field}__month"]
#         date_range = [f"{d.year}/{d.month}" for d in pd.date_range(start=start_date, end=end_date, freq="MS")]
#     else:
#         date_format = "%Y-%m-%d"
#         date_fields = [date_field]
#         date_range = [d.strftime("%Y-%m-%d") for d in pd.date_range(start=start_date, end=end_date)]

#     # フィルタ条件
#     filter_conditions = {f"{date_field}__gte": start_date, f"{date_field}__lte": end_date}
#     if category:
#         filter_conditions["category"] = category
#     if keyword:
#         filter_conditions["product__icontains"] = keyword

#     # データ取得 & 集計
#     sales_data = (
#         model.objects.filter(**filter_conditions)
#         .values("product", "model", *date_fields)
#         .annotate(total=Sum(agg_field))
#     )

#     # 横向きデータに変換
#     data_dict = defaultdict(lambda: {date: 0 for date in date_range})
#     for sale in sales_data:
#         key = (sale["product"], sale["model"])
#         sale_date = f"{sale[f'{date_field}__year']}/{sale[f'{date_field}__month']}" if period == "month" else str(sale[date_field])
#         if sale_date in date_range:
#             data_dict[key][sale_date] += sale["total"]

#     table_data = [{"name": k[0], "model": k[1], **v} for k, v in data_dict.items()]
    
#     return {"form": form, "date_range": date_range, "table_data": table_data}


# from django.apps import apps
# from django.db.models import Sum
# from collections import defaultdict
# import pandas as pd
# from .forms import SalesFilterForm

# def get_search_filters(request, model_name, date_field):
#     """ 検索フォームのデータを取得し、フィルタ条件を作成 """
#     form = SalesFilterForm(request.GET)

#     if not form.is_valid():
#         return {"form": form, "filter_conditions": None}  # フォームが無効ならそのまま返す

#     period = form.cleaned_data["period"]
#     start_date = form.cleaned_data["start_date"]
#     end_date = form.cleaned_data["end_date"]
#     category = form.cleaned_data["category"]
#     keyword = form.cleaned_data["keyword"]

#     filter_conditions = {f"{date_field}__gte": start_date, f"{date_field}__lte": end_date}
#     if category:
#         filter_conditions["category"] = category
#     if keyword:
#         filter_conditions["product__icontains"] = keyword

#     return {"form": form, "filter_conditions": filter_conditions, "period": period, "start_date": start_date, "end_date": end_date}

# def fetch_sales_data(request, model_name, date_field, agg_field):
#     """ 売上データを集計する """
#     filters = get_search_filters(request, model_name, date_field)
#     form = filters["form"]
#     filter_conditions = filters["filter_conditions"]

#     if not filter_conditions:
#         return {"form": form}

#     period = filters["period"]
#     start_date = filters["start_date"]
#     end_date = filters["end_date"]

#     model = apps.get_model("listapp", model_name)

#     # 日次 / 月次 の切り替え
#     if period == "month":
#         date_format = "%Y/%m"
#         date_fields = [f"{date_field}__year", f"{date_field}__month"]
#         date_range = [f"{d.year}/{d.month}" for d in pd.date_range(start=start_date, end=end_date, freq="MS")]
#     else:
#         date_format = "%Y-%m-%d"
#         date_fields = [date_field]
#         date_range = [d.strftime("%Y-%m-%d") for d in pd.date_range(start=start_date, end=end_date)]

#     # データ取得 & 集計
#     sales_data = (
#         model.objects.filter(**filter_conditions)
#         .values("product", "model", *date_fields)
#         .annotate(total=Sum(agg_field))
#     )

#     # 横向きデータに変換
#     data_dict = defaultdict(lambda: {date: 0 for date in date_range})
#     for sale in sales_data:
#         key = (sale["product"], sale["model"])
#         sale_date = f"{sale[f'{date_field}__year']}/{sale[f'{date_field}__month']}" if period == "month" else str(sale[date_field])
#         if sale_date in date_range:
#             data_dict[key][sale_date] += sale["total"]

#     table_data = [{"name": k[0], "model": k[1], **v} for k, v in data_dict.items()]
    
#     return {"form": form, "date_range": date_range, "table_data": table_data}

# from django.apps import apps
# from django.db.models import Sum
# from collections import defaultdict
# import pandas as pd
# from .forms import SalesFilterForm

# def get_search_filters(request, model_name, date_field):
#     """ 検索フォームのデータを取得し、フィルタ条件を作成（集計用） """
#     form = SalesFilterForm(request.GET)

#     if not form.is_valid():
#         return {"form": form, "filter_conditions": None}  # フォームが無効ならそのまま返す

#     period = form.cleaned_data["period"]
#     start_date = form.cleaned_data["start_date"]
#     end_date = form.cleaned_data["end_date"]
#     category = form.cleaned_data["category"]
#     keyword = form.cleaned_data["keyword"]

#     filter_conditions = {f"{date_field}__gte": start_date, f"{date_field}__lte": end_date}
#     if category:
#         filter_conditions["category"] = category
#     if keyword:
#         filter_conditions["product__icontains"] = keyword

#     return {
#         "form": form, 
#         "filter_conditions": filter_conditions, 
#         "period": period, 
#         "start_date": start_date, 
#         "end_date": end_date
#     }

# def get_list_filters(request, model_name, date_field):
#     """ 検索フォームのデータを取得し、フィルタ条件を作成（リスト表示用 / 集計単位なし） """
#     form = SalesFilterForm(request.GET)

#     if not form.is_valid():
#         return {"form": form, "filter_conditions": None}

#     start_date = form.cleaned_data["start_date"]
#     end_date = form.cleaned_data["end_date"]
#     category = form.cleaned_data["category"]
#     keyword = form.cleaned_data["keyword"]

#     filter_conditions = {f"{date_field}__gte": start_date, f"{date_field}__lte": end_date}
#     if category:
#         filter_conditions["category"] = category
#     if keyword:
#         filter_conditions["product__icontains"] = keyword

#     return {"form": form, "filter_conditions": filter_conditions}

# def fetch_sales_data(request, model_name, date_field, agg_field):
#     """ 売上データを集計する """
#     filters = get_search_filters(request, model_name, date_field)
#     form = filters["form"]
#     filter_conditions = filters["filter_conditions"]

#     if not filter_conditions:
#         return {"form": form}

#     period = filters["period"]
#     start_date = filters["start_date"]
#     end_date = filters["end_date"]

#     model = apps.get_model("listapp", model_name)

#     # 日次 / 月次 の切り替え
#     if period == "month":
#         date_format = "%Y/%m"
#         date_fields = [f"{date_field}__year", f"{date_field}__month"]
#         date_range = [f"{d.year}/{d.month}" for d in pd.date_range(start=start_date, end=end_date, freq="MS")]
#     else:
#         date_format = "%Y-%m-%d"
#         date_fields = [date_field]
#         date_range = [d.strftime("%Y-%m-%d") for d in pd.date_range(start=start_date, end=end_date)]

#     # データ取得 & 集計
#     sales_data = (
#         model.objects.filter(**filter_conditions)
#         .values("product", "model", *date_fields)
#         .annotate(total=Sum(agg_field))
#     )

#     # 横向きデータに変換
#     data_dict = defaultdict(lambda: {date: 0 for date in date_range})
#     for sale in sales_data:
#         key = (sale["product"], sale["model"])
#         sale_date = f"{sale[f'{date_field}__year']}/{sale[f'{date_field}__month']}" if period == "month" else str(sale[date_field])
#         if sale_date in date_range:
#             data_dict[key][sale_date] += sale["total"]

#     table_data = [{"name": k[0], "model": k[1], **v} for k, v in data_dict.items()]
    
#     return {"form": form, "date_range": date_range, "table_data": table_data}

from django.apps import apps
from django.db.models import Sum, Q
from collections import defaultdict
import pandas as pd
from .forms import SalesFilterForm

def get_search_filters(request, model_name, date_field, columns):
    """ 検索フォームのデータを取得し、フィルタ条件を作成 """
    form = SalesFilterForm(request.GET)

    if not form.is_valid():
        return {"form": form, "filter_conditions": None, "keyword_filter": None}

    period = form.cleaned_data.get("period")
    start_date = form.cleaned_data["start_date"]
    end_date = form.cleaned_data["end_date"]
    category = form.cleaned_data["category"]
    keyword = form.cleaned_data["keyword"]

    # 📌 月次の場合は「月の頭」からデータを取得
    if period == "month":
        start_date = start_date.replace(day=1)

    filter_conditions = {f"{date_field}__gte": start_date, f"{date_field}__lte": end_date}
    if category:
        filter_conditions["category"] = category

    # キーワード検索：すべてのカラムに対して部分一致検索
    keyword_filter = Q()
    if keyword:
        for column in columns:
            keyword_filter |= Q(**{f"{column}__icontains": keyword})

    return {
        "form": form, 
        "filter_conditions": filter_conditions, 
        "keyword_filter": keyword_filter, 
        "period": period, 
        "start_date": start_date, 
        "end_date": end_date
    }

def fetch_sales_data(request, model_name, date_field, agg_field, columns, is_list_view=False):
    """ 売上データを集計する """
    filters = get_search_filters(request, model_name, date_field, columns)
    form = filters["form"]
    filter_conditions = filters["filter_conditions"]
    keyword_filter = filters["keyword_filter"]

    if not filter_conditions:
        return {"form": form}

    period = filters["period"]
    start_date = filters["start_date"]
    end_date = filters["end_date"]

    model = apps.get_model("listapp", model_name)

    if is_list_view:
        date_range = [d.strftime("%y-%m-%d") for d in pd.date_range(start=start_date, end=end_date)]
        date_field = [date_field]
    else:
        priod = filters["period"]        

        # 日次 / 月次 の切り替え
        if period == "month":
            date_format = "%Y/%m"
            date_fields = [f"{date_field}__year", f"{date_field}__month"]
            # 月ごとのdate_rangeを作成
            date_range = [d.strftime("%Y-%m") for d in pd.date_range(start=start_date, end=end_date, freq="MS")]
        else:
            date_format = "%Y-%m-%d"
            date_fields = [date_field]
            # 日ごとのdate_rangeを作成
            date_range = [d.strftime("%Y-%m-%d") for d in pd.date_range(start=start_date, end=end_date)]

    # データ取得 & 集計（キーワード検索を適用）
    sales_data = (
        model.objects.filter(**filter_conditions).filter(keyword_filter)
        .values("channel", "product", "model", *date_fields)
        .annotate(total=Sum(agg_field))
    )
    print("個々の値", sales_data)

    # 横向きデータに変換
    data_dict = defaultdict(lambda: {date: 0 for date in date_range})

    for sale in sales_data:
        if is_list_view:
            sale_date = str(sale[date_field])
        else:       
            # 月次の場合、年月をキーとして使う
            if period == "month":
                sale_date = f"{sale['purchase_date__year']}-{sale['purchase_date__month']:02d}"
            else:
                # 日次の場合、そのまま日付を使う
                sale_date = str(sale[date_field])
            
            # 集計データがdate_range内に含まれる場合、売上を加算
            if sale_date in date_range:
                data_dict[(sale["channel"],sale["product"], sale["model"])][sale_date] += sale["total"]
    print("データでぃくと",data_dict.items())

    # テーブルデータの作成
    table_data = [{"channel":k[0], "name": k[1], "model": k[2], **v} for k, v in data_dict.items()]
    #print(table_data)
    return {"form": form, "date_range": date_range, "table_data": table_data}

def get_list_filters(request, model_name, date_field, columns):
    """ 検索フォームのデータを取得し、フィルタ条件を作成（リスト表示用） """
    filters = get_search_filters(request, model_name, date_field, columns)
    return {"form": filters["form"], "filter_conditions": filters["filter_conditions"], "keyword_filter": filters["keyword_filter"]}
