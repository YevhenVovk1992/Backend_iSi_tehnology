from django.db.models import Q
from rest_framework import viewsets, mixins, status, generics
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from application import models, serializer


# Create your views here.
class ThreadDetail(mixins.CreateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    """

    """
    queryset = models.Thread.objects.all()
    serializer_class = serializer.ThreadSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ThreadList(generics.ListAPIView):
    """

    """
    queryset = models.Thread.objects.all()
    serializer_class = serializer.ThreadSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = models.Thread.objects.filter(
            Q(participants__first_user=user_id) | Q(participants__second_user=user_id)
        ).all()
        return queryset


class MessageViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    """

    """
    queryset = models.Message.objects.all()
    serializer_class = serializer.MessageSerializer

    def get_queryset(self):
        queryset = models.Message.objects.filter(thread=self.request.data.get('thread')).all()
        return queryset

    def create(self, request, *args, **kwargs):
        user_id = self.request.user.id
        data = request.data
        data['sender'] = user_id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MessageStatus(mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = models.Message.objects.all()
    serializer_class = serializer.MessageSerializer

    def put(self, request, *args, **kwargs):
        if request.data.get('is_read', None):
            return self.update(request, *args, partial=True, **kwargs)
        return Response({"error": "is_read field not specified"})
