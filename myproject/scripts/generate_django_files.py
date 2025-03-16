import yaml
import os

CONFIG_PATH = "/home/yuka/Projects/test/django_datalist/myproject/config/config.yaml"
APP_NAME = "listapp"
TEMPLATE_DIR = f"{APP_NAME}/templates"
VIEW_DIR = f"{APP_NAME}/views"
URLS_PATH = f"{APP_NAME}/urls.py"

# 設定ファイルを読み込む
with open(CONFIG_PATH, "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

url_patterns = []

for table in config["tables"]:
    table_name = table["name"].lower()
    title = table["title"]
    search_conditions = table["search_conditions"]
    columns = table["columns"]

    os.makedirs(f"{TEMPLATE_DIR}/{table_name}", exist_ok=True)
    os.makedirs(VIEW_DIR, exist_ok=True)

    # --- search.html の作成 ---
    search_html = f"""<h2>{title} - 検索</h2>
<form action="/{table_name}/list/" method="GET">
"""

    for condition in search_conditions:
        if condition["type"] == "month_range":
            search_html += """<label>開始月: <input type="month" name="start_month"></label>
<label>終了月: <input type="month" name="end_month"></label>
"""
        elif condition["type"] == "day_range":
            search_html += """<label>開始日: <input type="date" name="start_date"></label>
<label>終了日: <input type="date" name="end_date"></label>
"""
        elif condition["type"] == "customer_id":
            search_html += """<label>顧客番号: <input type="text" name="customer_id"></label>
"""

    search_html += """<button type="submit">検索</button>
</form>
"""

    with open(f"{TEMPLATE_DIR}/{table_name}/search.html", "w", encoding="utf-8") as f:
        f.write(search_html)

    # --- list.html の作成 ---
    list_html = f"""<h2>{title} - 一覧</h2>
<table border="1">
    <thead>
        <tr>
"""

    for column in columns:
        list_html += f"            <th>{column['title']}</th>\n"

    list_html += "        </tr>\n    </thead>\n    <tbody>\n        {% for row in data %}\n        <tr>\n"

    for column in columns:
        list_html += f"            <td>{{{{ row.{column['field']} }}}}</td>\n"

    list_html += """        </tr>
        {% endfor %}
    </tbody>
</table>
"""

    with open(f"{TEMPLATE_DIR}/{table_name}/list.html", "w", encoding="utf-8") as f:
        f.write(list_html)

    # --- views.py の作成 ---
    view_code = f"""from django.shortcuts import render
from .models import {table['name']}  # 既存のモデルを使用

def {table_name}_list(request):
    filters = {{}}

"""

    for condition in search_conditions:
        if condition["type"] == "month_range":
            view_code += """    if request.GET.get("start_month") and request.GET.get("end_month"):
        filters["order_date__year__gte"], filters["order_date__month__gte"] = map(int, request.GET["start_month"].split("-"))
        filters["order_date__year__lte"], filters["order_date__month__lte"] = map(int, request.GET["end_month"].split("-"))

"""
        elif condition["type"] == "day_range":
            view_code += """    if request.GET.get("start_date") and request.GET.get("end_date"):
        filters["order_date__range"] = [request.GET["start_date"], request.GET["end_date"]]

"""
        elif condition["type"] == "customer_id":
            view_code += """    if request.GET.get("customer_id"):
        filters["customer_id"] = request.GET["customer_id"]

"""

    view_code += f"""    data = {table['name']}.objects.filter(**filters)
    return render(request, "{table_name}/list.html", {{"data": data}})

"""

    with open(f"{VIEW_DIR}/{table_name}.py", "w", encoding="utf-8") as f:
        f.write(view_code)

    # --- URLパターンを保存 ---
    url_patterns.append(f'    path("{table_name}/list/", {table_name}_list, name="{table_name}_list"),')

# --- urls.py の作成 ---
urls_code = """from django.urls import path
"""

for table in config["tables"]:
    urls_code += f"from .views.{table['name'].lower()} import {table['name'].lower()}_list\n"

urls_code += "\nurlpatterns = [\n"
urls_code += "\n".join(url_patterns)
urls_code += "\n]\n"

with open(URLS_PATH, "w", encoding="utf-8") as f:
    f.write(urls_code)

print("Django のテンプレート・ビュー・URL を自動生成しました")
