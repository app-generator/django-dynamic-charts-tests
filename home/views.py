import json

import django
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from home.DynamicChart import DynamicChart
from home.models import *
from home.helpers import *


# Create your views here.


def index(request):
    # Page from the theme
    return render(request, 'pages/index.html')


def dyn_chart(request, model_name, chart_type, col_1, col_2=None, col_3=None):
    chart = DynamicChart("home.models." + model_name)
    if chart_type == "pie":
        content, status = chart.pie_render(column_name=col_1, report_start=col_2)
        return HttpResponse(content=content, status=status)
    else:
        content = loader.render_to_string(template_name="dyn_chart_template.html", context={
            'message': f"'{chart_type}' charts are not supported.",
            'successful': False,
        })
        return HttpResponse(content=content, status=400)
