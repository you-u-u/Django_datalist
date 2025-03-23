from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, TemplateView
from .models import SalesRecord
from .utils import fetch_sales_data, get_list_filters

COLUMNS = ["channel", "product", "model", "purchase_date", "quantity", "category"]  # 検索対象カラム

class Top(TemplateView):
    template_name = "top.html"
    
class SalesByProductView(View):
    def get(self, request):
        context = fetch_sales_data(request, model_name="SalesRecord", date_field="purchase_date", agg_field="quantity", columns=COLUMNS)
        return render(request, "listapp/sales_table.html", context)

class SalesList(ListView):
    template_name = "list/sales_list.html"
    model = SalesRecord

    


class SalesRecordList(ListView):
    template_name = "listapp/list.html"
    model = SalesRecord

    def get_queryset(self):
        """ 検索条件に基づいてフィルタリング """
        filters = get_list_filters(self.request, model_name="SalesRecord", date_field="purchase_date", columns=COLUMNS)
        filter_conditions = filters["filter_conditions"]
        keyword_filter = filters["keyword_filter"]

        if filter_conditions:
            return self.model.objects.filter(**filter_conditions).filter(keyword_filter)
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        """ 検索フォームをテンプレートに渡す """
        context = super().get_context_data(**kwargs)
        context.update(get_list_filters(self.request, model_name="SalesRecord", date_field="purchase_date", columns=COLUMNS))
        return context


from django.views.generic import ListView
from django.db.models import Q
from .models import SalesRecord
from .forms import SalesRecordSearchForm

class SalesRecordListView(ListView):
    model = SalesRecord  # どのモデルを使うか指定
    template_name = "listapp/sales_record_list.html"  # 使用するテンプレート
    context_object_name = "records"  # テンプレートで使う変数名
    
    def get_queryset(self):
        """データのフィルタリング処理"""
        queryset = super().get_queryset()  # `SalesRecord.objects.all()` と同じ
        form = SalesRecordSearchForm(self.request.GET)  # フォームの値を取得

        if form.is_valid():  # フォームが有効な場合のみ検索実行
            start_date = form.cleaned_data.get("start_date")
            end_date = form.cleaned_data.get("end_date")
            category = form.cleaned_data.get("category")
            search = form.cleaned_data.get("search")

            # 日付フィルタ
            if start_date:
                queryset = queryset.filter(purchase_date__gte=start_date)
            if end_date:
                queryset = queryset.filter(purchase_date__lte=end_date)

            # 区分フィルタ
            if category:
                queryset = queryset.filter(category=category)

            # あいまい検索
            if search:
                queryset = queryset.filter(
                    Q(product__icontains=search) |
                    Q(model__icontains=search) |
                    Q(channel__icontains=search)
                )

        return queryset  # フィルタリング後のデータを返す

    def get_context_data(self, **kwargs):
        """テンプレートに渡すデータ"""
        context = super().get_context_data(**kwargs)
        context["form"] = SalesRecordSearchForm(self.request.GET)  # フォームを渡す
        return context



# from django.shortcuts import render
# from django.views.generic import TemplateView, ListView
# from django.apps import apps
# from django.db.models import Sum
# from django.views import View
# from .forms import SalesFilterForm
# from collections import defaultdict
# from .models import SalesRecord
# import pandas as pd
# from .utils import fetch_sales_data, get_list_filters

# class Top(TemplateView):
#     template_name = "top.html"
    

# class SalesRecordList(ListView):
#     template_name = "listapp/list.html"
#     model = SalesRecord


#     def get_queryset(self):
#         """ 検索条件に基づいてフィルタリング """
#         filters = get_list_filters(self.request, model_name="SalesRecord", date_field="purchase_date", columns="columns")
#         filter_conditions = filters["filter_conditions"]

#         if filter_conditions:
#             return self.model.objects.filter(**filter_conditions)
#         return self.model.objects.all()

#     def get_context_data(self, **kwargs):
#         """ 検索フォームをテンプレートに渡す """
#         context = super().get_context_data(**kwargs)
#         context.update(get_list_filters(self.request, model_name="SalesRecord", date_field="purchase_date"))
#         return context


# class SalesByProductView(View):
#     def get(self, request):
#         columns = ["product", "model", "order_date", "quantity", "category"]  # 検索対象カラムを指定
#         context = fetch_sales_data(request, model_name="SalesRecord", date_field="order_date", agg_field="quantity", columns=columns)
#         return render(request, "listapp/sales_table.html", context)
    
# ここからモジュール化
# class SalesByProductView(View):
#     def get(self, request):
#         form = SalesFilterForm(request.GET)

#         if form.is_valid():
#             period = form.cleaned_data["period"]  # "day" or "month"
#             start_date = form.cleaned_data["start_date"]
#             end_date = form.cleaned_data["end_date"]
#             category = form.cleaned_data["category"]
#             keyword = form.cleaned_data["keyword"]

#             model = apps.get_model("listapp", "SalesRecord")

#             # 日次 / 月次 の切り替え
#             if period == "month":
#                 date_format = "%Y/%m"
#                 date_field = ["purchase_date__year", "purchase_date__month"]
#                 # 検索範囲内のすべての月を取得
#                 date_range = [f"{d.year}/{d.month}" for d in pd.date_range(start=start_date, end=end_date, freq="MS")]
#             else:
#                 date_format = "%Y-%m-%d"
#                 date_field = ["purchase_date"]
#                 # 検索範囲内のすべての日を取得
#                 date_range = [d.strftime("%Y-%m-%d") for d in pd.date_range(start=start_date, end=end_date)]

#             # フィルタ条件
#             filter_conditions = {
#                 "purchase_date__gte": start_date,
#                 "purchase_date__lte": end_date
#             }
#             if category:
#                 filter_conditions["category"] = category
#             if keyword:
#                 filter_conditions["product__icontains"] = keyword

#             # データ取得 & 集計
#             if period == "month":
#                 sales_data = (
#                     model.objects.filter(**filter_conditions)
#                     .values("product", "model", "purchase_date__year", "purchase_date__month")
#                     .annotate(total=Sum("quantity"))
#                 )
#             else:
#                 sales_data = (
#                     model.objects.filter(**filter_conditions)
#                     .values("product", "model", "purchase_date")
#                     .annotate(total=Sum("quantity"))
#                 )

#             # 横向きデータに変換（初期値はすべて0）
#             data_dict = defaultdict(lambda: {date: 0 for date in date_range})
#             for sale in sales_data:
#                 key = (sale["product"], sale["model"])
#                 if period == "month":
#                     sale_date = f"{sale['purchase_date__year']}/{sale['purchase_date__month']}"  # 修正
#                 else:
#                     sale_date = str(sale["purchase_date"])
                
#                 # sale_date が date_range に含まれている場合のみ代入
#                 if sale_date in date_range:
#                     data_dict[key][sale_date] += sale["total"]

#             # テンプレートに渡すデータ
#             table_data = [{"name": k[0], "model": k[1], **v} for k, v in data_dict.items()]

#             return render(
#                 request, 
#                 "listapp/sales_table.html", 
#                 {"form": form, "date_range": date_range, "table_data": table_data}
#             )

#         return render(request, "listapp/sales_table.html", {"form": form})

# ここまでをモジュール化
# ---------------------------------------------------------------------------

# # 一覧画面（クロス集計）
# def salesrecord_list(request):
#     start_date = request.GET.get('start_date')
#     end_date = request.GET.get('end_date')
#     print("はじあり",start_date)

#     # デフォルトで当月の1日〜月末を設定
#     if not start_date:
#         start_date = datetime.today().replace(day=1).strftime('%Y-%m-%d')
#     if not end_date:
#         end_date = datetime.today().strftime('%Y-%m-%d')
#     print("デフォルト",start_date)
#     print(type("start_data"))

#     start_date = datetime.strptime(start_date, "%Y-%m-%d")
#     end_date = datetime.strptime(end_date, "%Y-%m-%d")
#     print("syrptimeした",start_date)
#     print(type("start_data"))


#     # 指定範囲内の月リストを作成
#     months = []
#     current_date = start_date
#     while current_date <= end_date:
#         months.append((current_date.year, current_date.month))
#         print(f"月：{months}")
#         current_date += timedelta(days=32)  # 次の月へ
#         current_date = current_date.replace(day=1)  # 月の最初の日に調整

#     # データ取得＆クロス集計
#     raw_data = SalesRecord.objects.filter(
#         purchase_date__range=[start_date, end_date]
#     # valuesで指定したデータを取得
#     ).values(
#         'channel', 'product', 'model', 'purchase_date__year', 'purchase_date__month'
#     # annotateで新しい属性を追加
#     ).annotate(
#         total_quantity=Sum('quantity')
#     )
#     print(f"取りたいデータ：{raw_data}")

#     # データを辞書に整理
#     data_dict = {}
#     for row in raw_data:
#         key = (row["channel"], row["product"], row["model"])
#         # print({key})
#         # {('amazon', 'mac book air', 'mac book air')}
#         if key not in data_dict:
#             data_dict[key] = {month: 0 for month in months}  # 各月の初期値 0
#         data_dict[key][(row["purchase_date__year"], row["purchase_date__month"])] = row["total_quantity"]

#     print(f"辞書型：{data_dict}")
#     # 辞書型：{('amazon', 'mac book air', 'mac book air'): {(2025, 1): 5, (2025, 2): 0, (2025, 3): 0}, ('量販店', 'Windows11', 'Windows11'): {(2025, 1): 1, (2025, 2): 0, (2025, 3): 0}}
#     print(f"辞書型アイテム：{data_dict.items()}")
#     # 辞書型アイテム：dict_items([(('amazon', 'mac book air', 'mac book air'), {(2025, 1): 5, (2025, 2): 0, (2025, 3): 0}), (('量販店', 'Windows11', 'Windows11'), {(2025, 1): 1, (2025, 2): 0, (2025, 3): 0})])

#     # テンプレートに渡すデータ形式
#     formatted_data = []

#     for (channel, product, model), values in data_dict.items():
#         row = {
#             "channel": channel,
#             "product": product,
#             "model": model,
#             "monthly_data": [values[month] for month in months]
#         }
#         formatted_data.append(row)
#         # print(f"ふぉーまっと：{formatted_data}")
#         # print(f"ふぉーまっと：type{formatted_data}")

#     # apiを使用する際はresposeを使用してJSON形式で返す必要がある
#     # return Response({
#     #     'data': formatted_data,
#     #     'months': months,
#     #     'start_date': start_date.strftime('%Y-%m-%d'),
#     #     'end_date': end_date.strftime('%Y-%m-%d')
#     # })

#     return render(request, 'listapp/sales_list.html', {
#         'data': formatted_data,
#         'months': months,
#         'start_date': start_date.strftime('%Y-%m-%d'),
#         'end_date': end_date.strftime('%Y-%m-%d')
#     })


# # import pandas as pd
# # from django.shortcuts import render
# # from django.db.models import Sum
# # from .models import SalesRecord
# # from datetime import datetime, timedelta

# # def salesrecord_list_pandas(request):
# #     # ① クエリパラメータ（start_date, end_date）を取得
# #     start_date = request.GET.get("start_date")
# #     end_date = request.GET.get("end_date")

# #     # ② start_date, end_date のデフォルト値（当月の1日〜今日）
# #     if not start_date:
# #         start_date = datetime.today().replace(day=1).strftime("%Y-%m-%d")
# #     if not end_date:
# #         end_date = datetime.today().strftime("%Y-%m-%d")

# #     # ③ 日付を datetime 型に変換
# #     start_date = datetime.strptime(start_date, "%Y-%m-%d")
# #     end_date = datetime.strptime(end_date, "%Y-%m-%d")

# #     # ④ 指定範囲の月リストを作成
# #     months = []
# #     current_date = start_date
# #     while current_date <= end_date:
# #         months.append((current_date.year, current_date.month))
# #         current_date += timedelta(days=32)
# #         current_date = current_date.replace(day=1)

# #     # ⑤ SalesRecord モデルからデータを取得
# #     raw_data = SalesRecord.objects.filter(
# #         purchase_date__range=[start_date, end_date]
# #     ).values("channel", "product", "model", "purchase_date", "quantity")

# #     # ⑥ クエリセットを Pandas の DataFrame に変換
# #     df = pd.DataFrame.from_records(raw_data)

# #     if df.empty:  # データがない場合
# #         return render(request, "listapp/sales_list.html", {
# #             "data": [],
# #             "months": months,
# #             "start_date": start_date.strftime("%Y-%m-%d"),
# #             "end_date": end_date.strftime("%Y-%m-%d"),
# #         })

# #     # ⑦ purchase_date を "年" と "月" に分割
# #     df["year"] = df["purchase_date"].dt.year
# #     df["month"] = df["purchase_date"].dt.month

# #     # ⑧ データの集計（groupby + sum）
# #     pivot_table = df.groupby(["channel", "product", "model", "year", "month"])["quantity"].sum().unstack(fill_value=0)

# #     # ⑨ 月ごとのデータをリストに変換
# #     formatted_data = []
# #     for (channel, product, model), row in pivot_table.groupby(level=[0, 1, 2]):
# #         formatted_row = {
# #             "channel": channel,
# #             "product": product,
# #             "model": model,
# #             "monthly_data": [row.get((year, month), 0) for year, month in months],
# #         }
# #         formatted_data.append(formatted_row)

# #     # ⑩ テンプレートにデータを渡して表示
# #     return render(request, "listapp/sales_list.html", {
# #         "data": formatted_data,
# #         "months": months,
# #         "start_date": start_date.strftime("%Y-%m-%d"),
# #         "end_date": end_date.strftime("%Y-%m-%d"),
# #     })

# from django.shortcuts import render
# from django.views import View
# from .utils import get_sales_data

# class SalesByProductView(View):
#     def get(self, request):
#         context = get_sales_data(request)  # 関数を呼び出す
#         return render(request, "listapp/sales_table.html", context)
