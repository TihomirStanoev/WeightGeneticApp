from rest_framework import generics
from rest_framework.generics import get_object_or_404
from master_data.models import Reference
from measurements.models import Batch, Measurement
from measurements.serializers import BatchSerializer, MeasurementSerializer


class BatchBaseView:
    serializer_class = BatchSerializer

    @property
    def _reference_material(self):
        return self.kwargs['reference']

    def get_queryset(self):
        return Batch.objects.select_related('reference').filter(reference__material=self._reference_material)


class BatchListCreateView(BatchBaseView, generics.ListCreateAPIView):
    def perform_create(self, serializer):
        reference = get_object_or_404(Reference, material=self._reference_material)
        serializer.save(reference=reference)


class BatchDetailView(BatchBaseView, generics.RetrieveUpdateDestroyAPIView):
    pass



class MeasurementBaseView:
    serializer_class = MeasurementSerializer

    @property
    def _batch_pk(self):
        return self.kwargs['batch_pk']

    def get_queryset(self):
        return Measurement.objects.select_related('batch').filter(batch_id=self._batch_pk)


class MeasurementListCreateView(MeasurementBaseView, generics.ListCreateAPIView):
    def perform_create(self, serializer):
        batch = get_object_or_404(Batch, pk=self._batch_pk)
        serializer.save(batch=batch)


class MeasurementDetailView(MeasurementBaseView, generics.RetrieveUpdateDestroyAPIView):
    pass