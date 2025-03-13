import yaml
import os

CONFIG_PATH = "config/config.yaml"

# 設定ファイルを読み込む
with open(CONFIG_PATH, "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

for table in config["tables"]:
    model_name = table["name"].lower()
    template_dir = f"your_app/templates/{model_name}"
    os.makedirs(template_dir, exist_ok=True)

    # 検索フォーム（search.html）
    search_form_html = f"""<h2>{table['title']} - 検索</h2>
<form action="/{model_name}/list/" method="GET">
"""

    if "month_range" in [cond["type"] for cond in table["search_conditions"]]:
        search_form_html += """<label>開始月: <input type="month" name="start_month"></label>
<label>終了月: <input type="month" name="end_month"></label>
"""

    if "day_range" in [cond["type"] for cond in table["search_conditions"]]:
        search_form_html += """<label>開始日: <input type="date" name="start_date"></label>
<label>終了日: <input type="date" name="end_date"></label>
"""

    if "customer_id" in [cond["type"] for cond in table["search_conditions"]]:
        search_form_html += """<label>顧客番号: <input type="text" name="customer_id"></label>
"""

    search_form_html += """<button type="submit">検索</button>
</form>
"""
    with open(f"{template_dir}/search.html", "w", encoding="utf-8") as f:
        f.write(search_form_html)
