from django.urls import path

from .views import (index, BbByRubricView,
                    BbCreateView, BbDetailView)


app_name = 'bboard'

urlpatterns = [
    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    path('add/', BbCreateView.as_view(), name='add'),
    path('<int:rubric_id>/', BbByRubricView.as_view(), name='by_rubric'),

    path('', index, name='index'),
]
