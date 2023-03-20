import json

from django.http import HttpResponse, request
from django.shortcuts import render
from django.template import loader

from home.helpers import find_model_class_by_path

import django.db.models
from django import views
from pathlib import Path


class DynamicChart(views.View):

    def __init__(self, model_class_path: str = None, **kwargs):
        # model_class_path's format:module_path.class_name
        super().__init__(**kwargs)
        if model_class_path is None:
            return
        self.model_class_path = model_class_path
        self.model_class: django.db.models.Manager = find_model_class_by_path(model_class_path)
        self.model_name = self.model_class_path.split('.')[-1]

    def pie_render(self, column_name, report_start):
        context = {'chart_type': "pie"}
        columns_names = [f.name for f in self.model_class._meta.get_fields()]
        try:
            report_start = int(report_start)
        except ValueError:
            return loader.render_to_string(template_name="dyn_chart_template.html", context={
                'message': f"{report_start} must be an integer number.",
                'successful': False,
            }), 400

        if column_name in columns_names:
            context['label'] = column_name
            if report_start is None:
                data = list(self.model_class.objects.values_list(column_name, flat=True))
            else:
                data = self.model_class.objects.order_by("-id").values_list(column_name, flat=True)[:report_start][
                       ::-1]
            context['successful'] = True
            context['data'] = data
            print(context)
            return loader.render_to_string(template_name="dyn_chart_template.html", context=context), 200
        return loader.render_to_string(template_name="dyn_chart_template.html", context={
            'message': f"{column_name} is not a {self.model_name}'s attribute.",
            'successful': False,
        }), 400
