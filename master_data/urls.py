from django.urls import path, include
from master_data import views



profile_urlpatterns = [
    path('', views.ProfileListCreateView.as_view(), name='profile-list'),
    path('<str:profile_code>/', views.ProfileDetailView.as_view(), name='profile-detail'),
]

workpieces_urlpatterns = [
    path('', views.WorkpieceListCreateView.as_view(), name='workpiece-list'),
    path('<str:workpiece_material>/', views.WorkpieceDetailView.as_view(),
         name='workpiece-detail'),
]

references_urlpatterns = [
    path('', views.ReferenceListCreateView.as_view(), name='reference-list'),
    path('<str:reference_material>/', views.ReferenceDetailView.as_view(), name='reference-detail'),

]

urlpatterns = [
    path('profiles/', include(profile_urlpatterns)),
    path('profiles/<str:profile_code>/workpieces/', include(workpieces_urlpatterns)),
    path('profiles/<str:profile_code>/workpieces/<str:workpiece_material>/references/', include(references_urlpatterns)),
]