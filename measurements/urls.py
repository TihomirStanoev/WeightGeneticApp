from django.urls import path, include
from measurements import views



batch_urlpatterns = [
    path('', views.BatchListCreateView.as_view(), name='batch-list'),
    path('<int:pk>/', views.BatchDetailView.as_view(), name='batch-detail'),
]

measurement_urlpatterns = [
    path('', views.MeasurementListCreateView.as_view(), name='measurement-list'),
    path('<int:pk>/', views.MeasurementDetailView.as_view(), name='measurement-detail'),

]



urlpatterns = [
    path('references/<str:reference>/batches/', include(batch_urlpatterns)),
    path('references/<str:reference>/batches/<int:batch_pk>/measurements/', include(measurement_urlpatterns)),
]