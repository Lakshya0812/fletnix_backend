from django.urls import path
from . import views

urlpatterns = [
    path('' , views.index),
    # path('show-list/' , views.show_list)
]