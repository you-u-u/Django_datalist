from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.views import View


class MyView(View):
    def get(self, request):
        return HttpResponse("Hello, World!")

class Top(TemplateView):
  template_name = "top.html"