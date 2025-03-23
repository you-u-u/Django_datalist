# from django import forms

# class SalesFilterForm(forms.Form):
#     PERIOD_CHOICES = [
#         ("day", "日次"),
#         ("month", "月次"),
#     ]

#     period = forms.ChoiceField(choices=PERIOD_CHOICES, required=True, label="集計単位")
#     start_date = forms.DateField(
#         required=True, 
#         widget=forms.widgets.DateInput(attrs={"type": "date"})
#     )
#     end_date = forms.DateField(
#         required=True, 
#         widget=forms.widgets.DateInput(attrs={"type": "date"})
#     )
#     category = forms.ChoiceField(
#         choices=[("", "すべて"), ("PC", "PC"), ("SE品", "SE品")],
#         required=False,
#         label="区分"
#     )
#     keyword = forms.CharField(
#         required=False, 
#         label="キーワード", 
#         widget=forms.TextInput(attrs={"placeholder": "商品名を入力"})
#     )

# 動的に検索画面を定義
from django import forms

class SalesFilterForm(forms.Form):
    PERIOD_CHOICES = [
        ("day", "日次"),
        ("month", "月次"),
    ]

    period = forms.ChoiceField(choices=PERIOD_CHOICES, required=True, label="集計単位")
    start_date = forms.DateField(
        required=True, 
        widget=forms.widgets.DateInput(attrs={"type": "date"})
    )
    end_date = forms.DateField(
        required=True, 
        widget=forms.widgets.DateInput(attrs={"type": "date"})
    )
    category = forms.ChoiceField(
        choices=[("", "すべて"), ("PC", "PC"), ("SE品", "SE品")],
        required=False,
        label="区分"
    )
    keyword = forms.CharField(
        required=False, 
        label="キーワード", 
        widget=forms.TextInput(attrs={"placeholder": "商品名を入力"})
    )
