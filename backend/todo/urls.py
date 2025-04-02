from django.urls import path, include

from todo.views import MyView

urlpatterns = [
  path("mine/", MyView.as_view(), name="my-view"),
]