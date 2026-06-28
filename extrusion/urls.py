from django.urls import path, include
from extrusion import views




urlpatterns = [
    path('profiles/<str:profile_code>/cards/', views.ExtrusionListCreateView.as_view(), name='extrusion-list'),
    path('profiles/<str:profile_code>/cards/<str:card_no>/', views.ExtrusionDetailView.as_view(), name='extrusion-detail'),
]