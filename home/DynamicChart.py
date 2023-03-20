from django.db.models import Count
from django.template import loader

from home.helpers import find_model_class_by_path, get_timestamp_n_days_before, get_column_count

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
        self.model_name = self.model_class_path.split('.')[-1]

    def pie_render(self, column_name, report_start=None):
        context = {'chart_type': "pie"}
        columns_names = [f.name for f in self.model_class._meta.get_fields()]
        if column_name in columns_names:
            context['label'] = column_name
            if report_start is None:
                data, labels = get_column_count(model=self.model_class, column_name=column_name)
            else:
                try:
                    report_start = int(report_start)
                except ValueError:
                    return loader.render_to_string(template_name="dyn_chart_template.html", context={
                        'message': f"The last argument in the url must be an integer but you provided '{report_start}'",
                        'successful': False,
                    }), 400
                if report_start < 0:
                    return loader.render_to_string(template_name="dyn_chart_template.html", context={
                        'message': f"The last argument in the url must be a positive integer but you provided '{report_start}'",
                        'successful': False,
                    }), 400
                data, labels = get_column_count(model=self.model_class, column_name=column_name,
                                                report_start=report_start)
            context['successful'] = True
            context['data'] = data
            context['labels'] = labels
            return loader.render_to_string(template_name="dyn_chart_template.html", context=context), 200
        return loader.render_to_string(template_name="dyn_chart_template.html", context={
            'message': f"'{column_name}' is not a {self.model_name}'s attribute.",
            'successful': False,
        }), 400
