import yaml
import os

# 設定ファイルを読み込む
CONFIG_PATH = "config/config.yaml"
with open(CONFIG_PATH, "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

# Djangoファイルを新規作成する
for table in config["tables"]:
    model_name = table["name"].lower()
    view_file = f"your_app/views/{model_name}_views.py"
    template_dir = f"your_app/templates/{model_name}"

    # フォルダ作成
    os.makedirs(template_dir, exist_ok=True)

    # 検索フォーム（search.html）
    search_form_html = f"""<h2>{table['title']} - 検索</h2>
<form action="/{model_name}/list/" method="GET">
"""
    if any(cond["type"] == "month_range" for cond in table["search_conditions"]):
        search_form_html += """<label>開始月: <input type="month" name="start_month"></label>
<label>終了月: <input type="month" name="end_month"></label>
"""
    if any(cond["type"] == "day_range" for cond in table["search_conditions"]):
        search_form_html += """<label>開始日: <input type="date" name="start_date"></label>
<label>終了日: <input type="date" name="end_date"></label>
"""
    if any(cond["type"] == "customer_id" for cond in table["search_conditions"]):
        search_form_html += """<label>顧客番号: <input type="text" name="customer_id"></label>
"""
    search_form_html += """<button type="submit">検索</button>
</form>
"""
    with open(f"{template_dir}/search.html", "w", encoding="utf-8") as f:
        f.write(search_form_html)

    # 一覧ページ（list.html）
    column_headers = "".join([f"<th>{col['title']}</th>\n" for col in table["columns"]])
    list_html = f"""<h2>{table['title']} - 一覧</h2>
<table border="1">
<tr>
{column_headers}
</tr>
{{% for item in data %}}
<tr>
""" + "".join([f"<td>{{{{ item.{col['field']} }}}}</td>\n" for col in table["columns"]]) + """
</tr>
{% empty %}
<tr><td colspan="5">データがありません</td></tr>
{% endfor %}
</table>
"""
    with open(f"{template_dir}/list.html", "w", encoding="utf-8") as f:
        f.write(list_html)

    # Djangoビュー（views.py）
    views_code = f"""from django.shortcuts import render
from django.db.models import Sum
from .models import {table["name"]}

def {model_name}_search(request):
    return render(request, '{model_name}/search.html')

def {model_name}_list(request):
    data = {table["name"]}.objects.all()
    return render(request, '{model_name}/list.html', {{ 'data': data }})
"""
    with open(view_file, "w", encoding="utf-8") as f:
        f.write(views_code)

print("Djangoファイルの生成が完了しました！")
