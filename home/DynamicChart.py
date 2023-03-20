from home.helpers import find_model_class_by_path, get_column_count, render_page, render_error

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

    def pie_render(self, column_name: str, report_start: int = None) -> tuple[str, int]:
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
                    return render_error(template_name="dyn_chart_template.html", message=
                    f"The last argument in the url must be an integer but you provided '{report_start}'",
                                        status=400)
                if report_start < 0:
                    return render_error(template_name="dyn_chart_template.html", message=
                    f"The last argument in the url must be a positive integer but you provided '{report_start}'",
                                        status=400)
                data, labels = get_column_count(model=self.model_class, column_name=column_name,
                                                report_start=report_start)
            context['successful'] = True
            context['data'] = data
            context['labels'] = labels
            return render_page(template_name="dyn_chart_template.html", context=context)
        return render_error(template_name="dyn_chart_template.html",
                            message=f"'{column_name}' is not among {self.model_name}'s attributes.", status=400)
