from django.urls import path, include
from extrusion import views




urlpatterns = [
    path('<str:profile_code>/', views.ExtrusionListCreateView.as_view(), name='extrusion-list'),
    path('<str:profile_code>/<str:card_no>/', views.ExtrusionDetailView.as_view(), name='extrusion-detail'),
]