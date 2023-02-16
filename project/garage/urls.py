from django.urls import path

from . import views

app_name = 'garage'
urlpatterns = [
    # ex: /motorcycle/
    path('', views.IndexView.as_view(), name='IndexView'),
    # ex: /motorcycle/5/
    path('<int:motorcycle_id>/', views.DetailView.as_view(), name='DetailView'),
]