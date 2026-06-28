from rest_framework import generics
from rest_framework.generics import get_object_or_404

from extrusion.models import Extrusion
from extrusion.serializers import ExtrusionSerializer
from master_data.models import Profile


class ExtrusionBaseView:
    serializer_class = ExtrusionSerializer
    lookup_field = 'card_no'

    @property
    def _profile_code(self):
        return self.kwargs['profile_code']

    def get_queryset(self):
        return Extrusion.objects.select_related('profile').filter(profile__code=self._profile_code)



class ExtrusionListCreateView(ExtrusionBaseView, generics.ListCreateAPIView):
    def perform_create(self, serializer):
        profile = get_object_or_404(Profile, code=self._profile_code)
        serializer.save(profile=profile)



class ExtrusionDetailView(ExtrusionBaseView, generics.RetrieveUpdateDestroyAPIView):
    pass
