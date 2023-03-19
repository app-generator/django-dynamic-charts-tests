import json

from django.http import HttpResponse, request
from django.shortcuts import render

from home.helpers import find_model_class_by_path

import django.db.models
from django import views


class DynamicChart(views.View):

    def __init__(self, model_class_path: str = None, **kwargs):
        # model_class_path's format:module_path.class_name
        super().__init__(**kwargs)
        if model_class_path is None:
            return
        self.model_class_path = model_class_path
        self.model_class: django.db.models.Manager = find_model_class_by_path(model_class_path)
        self.data: list = []
        self.chart_type = None
        self.column_name = None

    def pie(self, column_name, report_start):
        self.chart_type = 'pie'

        columns_names = [f.name for f in self.model_class._meta.get_fields()]

        if column_name in columns_names:

            self.column_name = column_name
            if report_start is None:
                self.data = list(self.model_class.objects.values_list(column_name, flat=True))
            else:
                self.data = self.model_class.objects.order_by("-id").values_list(column_name, flat=True)[:10][::-1]

            return True
        return False

    def render(self):
        context = {'chart_type': self.chart_type}
        if self.chart_type == 'pie':
            context['label'] = self.column_name
            context['data'] = self.data
            print(context)
            print("___________")
            return HttpResponse(request,  context)
        else:
            return HttpResponse(json.dumps({
                'message': f"{self.chart_type} charts are not supported.",
                'success': False
            }), status=400)
