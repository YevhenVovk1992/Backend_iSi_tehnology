from django.db.models import Q
from rest_framework import mixins, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from application import models, serializer


# Create your views here.
class ThreadDetail(mixins.CreateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    """
    This class creates a thread. If such a thread exists, then returns it to the user.
    The "delete" method deletes the thread if the user is in participants field
    """
    queryset = models.Thread.objects.all()
    serializer_class = serializer.ThreadSerializer

    def post(self, request, *args, **kwargs):
        user_id = request.user.id

        # Сheck the correctness of the data
        try:
            thread_user = request.data.get('participants')
            first_user = int(thread_user.get('first_user'))
            second_user = int(thread_user.get('second_user'))
        except ValueError:
            return Response({"error": "Data not valid"}, status=status.HTTP_400_BAD_REQUEST)

        # Сheck the user is specified in the thread
        if thread_user and user_id in (first_user, second_user):
            return self.create(request, *args, **kwargs)
        return Response({"error": "User not in participants"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user_id = request.user.id
        instance = self.get_object()

        # Сheck the user is specified in the thread
        if user_id in instance.participants.values():
            instance_id = instance.id
            self.perform_destroy(instance)
            return Response({"successful": f"delete {instance_id} thread"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "User not in participants"}, status=status.HTTP_400_BAD_REQUEST)


class ThreadList(generics.ListAPIView):
    """
    This class for getting thread for an authorized user
    """
    queryset = models.Thread.objects.all()
    serializer_class = serializer.ThreadWithMessagesSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = models.Thread.objects.filter(
            Q(participants__first_user=user_id) | Q(participants__second_user=user_id)
        ).all()
        return queryset


class MessageViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    """
    The class for receiving messages on a given thread
    """
    queryset = models.Message.objects.all()
    serializer_class = serializer.MessageSerializer

    def get_queryset(self):
        try:
            get_id = int(self.request.data['thread'])
            queryset = models.Message.objects.filter(thread=get_id).all()
        except ValueError:
            queryset = []
        return queryset

    def create(self, request, *args, **kwargs):
        message_data = {}
        user_id = self.request.user.id
        try:
            thread_id = int(request.data['thread'])
            message_data['text'] = request.data.get('text')
            message_data['thread'] = thread_id
        except ValueError:
            return Response({"error": "data not valid"}, status=status.HTTP_400_BAD_REQUEST)
        thread = models.Thread.objects.filter(id=thread_id).first()

        # Сheck the user is specified in the thread
        if thread and user_id in thread.participants.values():
            message_data['sender'] = user_id
            serializer = self.get_serializer(data=message_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({"error": "user not in participants"}, status=status.HTTP_400_BAD_REQUEST)


class MessageStatus(mixins.UpdateModelMixin, generics.GenericAPIView):
    """
    Message status update
    """
    queryset = models.Message.objects.all()
    serializer_class = serializer.MessageSerializer

    def put(self, request, *args, **kwargs):
        user_id = request.user.id
        try:
            status_atr = request.data.get('is_read')
            thread = int(request.data.get('thread'))
        except ValueError:
            return Response({"error": "data not valid"}, status=status.HTTP_400_BAD_REQUEST)
        instance = self.get_object()

        # Сheck the correctness of the data
        if status_atr == 'true' and instance.thread.id == thread:

            # Сheck the user is specified in the thread
            if user_id in instance.thread.participants.values():
                return self.update(request, *args, partial=True, **kwargs)
            return Response({"error": "user not in thread"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "is_read field not specified or message has other thread"}, status=status.HTTP_400_BAD_REQUEST)


class UnreadMessage(APIView):
    """
    The class for getting the number of unread messages
    """
    def get(self, request):
        user_id = request.user.id
        try:
            thread = int(request.data.get('thread'))
        except ValueError:
            return Response({"error": "data not valid"}, status=status.HTTP_400_BAD_REQUEST)
        thread_obj = models.Thread.objects.filter(id=thread).first()

        # Сheck the user is specified in the thread
        if user_id in thread_obj.participants.values():
            queryset = models.Message.objects.filter(thread=thread, is_read=False).exclude(sender=user_id).count()
            return Response({"unread message": str(queryset)}, status=status.HTTP_201_CREATED)
