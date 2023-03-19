import json

import django
from django.shortcuts import render
from django.http import HttpResponse

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
        if chart.pie(column_name=col_1, report_start=col_2):
            return chart.render()

    else:
        return HttpResponse(json.dumps({
            'message': f"{chart_type} charts are not supported.",
            'success': False
        }), status=400)
