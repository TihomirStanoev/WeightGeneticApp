from rest_framework import generics
from rest_framework.generics import get_object_or_404

from master_data.models import Profile, Workpiece, Reference
from master_data.serializers import ProfileSerializer, WorkpieceSerializer, ReferenceSerializer


class ProfileBaseView:
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    lookup_url_kwarg = 'profile_code'
    lookup_field = 'code'


class ProfileListCreateView(ProfileBaseView, generics.ListCreateAPIView):
    pass


class ProfileDetailView(ProfileBaseView, generics.RetrieveUpdateDestroyAPIView):
    pass



class WorkpieceBaseView:
    serializer_class = WorkpieceSerializer
    lookup_url_kwarg = 'workpiece_material'
    lookup_field = 'material'

    @property
    def _profile_code(self):
        return self.kwargs['profile_code']

    def get_queryset(self):
        return Workpiece.objects.select_related('profile').filter(profile__code=self._profile_code)



class WorkpieceListCreateView(WorkpieceBaseView, generics.ListCreateAPIView):
    def perform_create(self, serializer):
        profile = get_object_or_404(Profile, code=self._profile_code)
        serializer.save(profile=profile)



class WorkpieceDetailView(WorkpieceBaseView, generics.RetrieveUpdateDestroyAPIView):
    pass



class ReferenceBaseView:
    serializer_class = ReferenceSerializer
    lookup_url_kwarg = 'reference_material'
    lookup_field = 'material'


    @property
    def _workpiece_material(self):
        return self.kwargs['workpiece_material']

    @property
    def _profile_code(self):
        return self.kwargs['profile_code']


    def get_queryset(self):
        return Reference.objects.select_related('workpiece').filter(workpiece__material=self._workpiece_material, workpiece__profile__code=self._profile_code)



class ReferenceListCreateView(ReferenceBaseView, generics.ListCreateAPIView):
    def perform_create(self, serializer):
        workpiece = get_object_or_404(Workpiece, material=self._workpiece_material)
        serializer.save(workpiece=workpiece)



class ReferenceDetailView(ReferenceBaseView, generics.RetrieveUpdateDestroyAPIView):
    pass





