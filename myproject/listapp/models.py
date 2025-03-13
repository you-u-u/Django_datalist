from django.db import models

class SalesRecord(models.Model):
    channel = models.CharField(max_length=100, verbose_name="販売経路")
    product = models.CharField(max_length=100, verbose_name="商品")
    model = models.CharField(max_length=100, verbose_name="モデル")
    purchase_date = models.DateField(verbose_name="購入日")
    quantity = models.PositiveIntegerField(verbose_name="購入数")

    def __str__(self):
        return f"{self.product} - {self.model} ({self.purchase_date})"


from django.db import models

class OrderHistory(models.Model):
    order_channel = models.CharField(max_length=255, verbose_name="注文経路")
    product_name = models.CharField(max_length=255, verbose_name="商品名")
    category = models.CharField(max_length=255, verbose_name="カテゴリ")
    order_date = models.DateField(verbose_name="注文日")
    customer_id = models.CharField(max_length=50, null=True, blank=True, verbose_name="顧客番号")
    order_quantity = models.PositiveIntegerField(verbose_name="注文数")

    def __str__(self):
        return f"{self.product_name} - {self.order_quantity}個 ({self.order_date})"

    