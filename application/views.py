from rest_framework import viewsets, mixins, status, generics

from application import models, serializer


# Create your views here.
class ThreadDetail(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView
):
    """

    """
    queryset = models.Thread.objects.all()
    serializer_class = serializer.ThreadSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)