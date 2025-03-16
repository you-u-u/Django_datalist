from django.shortcuts import render
from django.db.models import Sum
from .models import SalesRecord
from datetime import datetime, timedelta

# 検索画面
def salesrecord_search(request):
    return render(request, 'listapp/search.html')

# 一覧画面（クロス集計）
def salesrecord_list(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # # デフォルトで当月の1日〜月末を設定
    # if not start_date:
    #     start_date = datetime.today().replace(day=1).strftime('%Y-%m-%d')
    # if not end_date:
    #     end_date = datetime.today().strftime('%Y-%m-%d')

    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    # 指定範囲内の月リストを作成
    months = []
    current_date = start_date
    while current_date <= end_date:
        months.append((current_date.year, current_date.month))
        print(f"月：{months}")
        current_date += timedelta(days=32)  # 次の月へ
        current_date = current_date.replace(day=1)  # 月の最初の日に調整

    # データ取得＆クロス集計
    raw_data = SalesRecord.objects.filter(
        purchase_date__range=[start_date, end_date]
    # valuesで指定したデータを取得
    ).values(
        'channel', 'product', 'model', 'purchase_date__year', 'purchase_date__month'
    # annotateで新しい属性を追加
    ).annotate(
        total_quantity=Sum('quantity')
    )
    print(f"取りたいデータ：{raw_data}")

    # データを辞書に整理
    data_dict = {}
    for row in raw_data:
        key = (row["channel"], row["product"], row["model"])
        print({key})
        # {('amazon', 'mac book air', 'mac book air')}
        if key not in data_dict:
            data_dict[key] = {month: 0 for month in months}  # 各月の初期値 0
        data_dict[key][(row["purchase_date__year"], row["purchase_date__month"])] = row["total_quantity"]

    print(f"辞書型：{data_dict}")
    # 辞書型：{('amazon', 'mac book air', 'mac book air'): {(2025, 1): 5, (2025, 2): 0, (2025, 3): 0}, ('量販店', 'Windows11', 'Windows11'): {(2025, 1): 1, (2025, 2): 0, (2025, 3): 0}}
    print(f"辞書型アイテム：{data_dict.items()}")
    # 辞書型アイテム：dict_items([(('amazon', 'mac book air', 'mac book air'), {(2025, 1): 5, (2025, 2): 0, (2025, 3): 0}), (('量販店', 'Windows11', 'Windows11'), {(2025, 1): 1, (2025, 2): 0, (2025, 3): 0})])

    # テンプレートに渡すデータ形式
    formatted_data = []

    for (channel, product, model), values in data_dict.items():
        row = {
            "channel": channel,
            "product": product,
            "model": model,
            "monthly_data": [values[month] for month in months]
        }
        formatted_data.append(row)
        print(f"ふぉーまっと：{formatted_data}")
        print(f"ふぉーまっと：type{formatted_data}")



    return render(request, 'listapp/sales_list.html', {
        'data': formatted_data,
        'months': months,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d')
    })


import pandas as pd
from django.shortcuts import render
from django.db.models import Sum
from .models import SalesRecord
from datetime import datetime, timedelta

def salesrecord_list_pandas(request):
    # ① クエリパラメータ（start_date, end_date）を取得
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    # ② start_date, end_date のデフォルト値（当月の1日〜今日）
    if not start_date:
        start_date = datetime.today().replace(day=1).strftime("%Y-%m-%d")
    if not end_date:
        end_date = datetime.today().strftime("%Y-%m-%d")

    # ③ 日付を datetime 型に変換
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    # ④ 指定範囲の月リストを作成
    months = []
    current_date = start_date
    while current_date <= end_date:
        months.append((current_date.year, current_date.month))
        current_date += timedelta(days=32)
        current_date = current_date.replace(day=1)

    # ⑤ SalesRecord モデルからデータを取得
    raw_data = SalesRecord.objects.filter(
        purchase_date__range=[start_date, end_date]
    ).values("channel", "product", "model", "purchase_date", "quantity")

    # ⑥ クエリセットを Pandas の DataFrame に変換
    df = pd.DataFrame.from_records(raw_data)

    if df.empty:  # データがない場合
        return render(request, "listapp/sales_list.html", {
            "data": [],
            "months": months,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
        })

    # ⑦ purchase_date を "年" と "月" に分割
    df["year"] = df["purchase_date"].dt.year
    df["month"] = df["purchase_date"].dt.month

    # ⑧ データの集計（groupby + sum）
    pivot_table = df.groupby(["channel", "product", "model", "year", "month"])["quantity"].sum().unstack(fill_value=0)

    # ⑨ 月ごとのデータをリストに変換
    formatted_data = []
    for (channel, product, model), row in pivot_table.groupby(level=[0, 1, 2]):
        formatted_row = {
            "channel": channel,
            "product": product,
            "model": model,
            "monthly_data": [row.get((year, month), 0) for year, month in months],
        }
        formatted_data.append(formatted_row)

    # ⑩ テンプレートにデータを渡して表示
    return render(request, "listapp/sales_list.html", {
        "data": formatted_data,
        "months": months,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
    })
