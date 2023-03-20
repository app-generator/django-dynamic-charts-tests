from django.urls import path

from . import views
from .views import dyn_chart

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:model_name>/<str:chart_type>/<str:col_1>', dyn_chart),
    path('<str:model_name>/<str:chart_type>/<str:col_1>/<str:col_2>', dyn_chart)
]
