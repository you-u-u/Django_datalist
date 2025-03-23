from django import template

# Djangoにカスタムフィルターを登録
register = template.Library()

# キーが存在すればそのキーの値を返す、なければ０を返す
# | これはパイプと呼ばれ左の値を右のフィルター関数に渡すことができる
# Djangoのテンプレートエンジンでは（）を使用して呼び出すことができない
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, 0)  # デフォルトは0
