import importlib
from datetime import datetime
from typing import Tuple
import django.db.models
from django.db.models import Count
from django.template import loader


def find_model_class_by_path(model_class_path: str) -> django.db.models.Manager:
    # model_class_path's format:module_path.class_name
    model_name = model_class_path.split('.')[-1]
    model_import = model_class_path.replace('.' + model_name, '')

    module = importlib.import_module(model_import)
    class_db_manager = getattr(module, model_name)

    return class_db_manager


def get_timestamp_n_days_before(days: int) -> float:
    now = datetime.now().timestamp()
    return now - days * 86400


def get_column_count(model: django.db.models.Manager, column_name: str, report_start: int = -1
                     ) -> Tuple[list, list]:
    if report_start != -1:
        start_timestamp = get_timestamp_n_days_before(report_start)
        result = (model.objects
                  .filter(purchase_date__gt=start_timestamp)
                  .values(column_name)
                  .annotate(count=Count(column_name))
                  .order_by())
    else:
        result = (model.objects
                  .values(column_name)
                  .annotate(count=Count(column_name))
                  .order_by())
    column_values = []
    counts = []
    for dictionary in result:
        column_values.append(dictionary[column_name])
        counts.append(dictionary[column_name])
    return column_values, counts


def render_error(template_name: str, message: str, status: int) -> tuple[str, int]:
    return loader.render_to_string(template_name=template_name, context={
        'message': message,
        'successful': False,
    }), status


def render_page(template_name: str, context: dict) -> tuple[str, int]:
    return loader.render_to_string(template_name=template_name, context=context), 200
