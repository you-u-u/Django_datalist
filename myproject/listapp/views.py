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
        if key not in data_dict:
            data_dict[key] = {month: 0 for month in months}  # 各月の初期値 0
        data_dict[key][(row["purchase_date__year"], row["purchase_date__month"])] = row["total_quantity"]

    print(f"辞書型：{data_dict}")
    print(f"辞書型アイテム：{data_dict.items()}")



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

    return render(request, 'listapp/sales_list.html', {
        'data': formatted_data,
        'months': months,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d')
    })

