from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, Friend, FriendRequest
from .serializers import UserSerializer, FriendSerializer, FriendRequestSerializer

class UserRegistration(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FriendRequestList(generics.ListCreateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer

    def post(self, request, *args, **kwargs):
        from_user = request.user
        to_user_id = request.data.get('to_user')

        try:
            to_user = User.objects.get(id=to_user_id)
        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)

        friend_request = FriendRequest.objects.create(from_user=from_user, to_user=to_user)
        serializer = self.get_serializer(friend_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class FriendRequestDetail(generics.RetrieveDestroyAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer

    def put(self, request, *args, **kwargs):
        friend_request = self.get_object()
        if friend_request.to_user != request.user:
            return Response({'error': 'Вы не можете изменять этот запрос в друзья'}, status=status.HTTP_403_FORBIDDEN)

        action = request.data.get('action')

        if action == 'accept':
            friend_request.accept()
            return Response({'message': 'Запрос в друзья принят'}, status=status.HTTP_200_OK)
        elif action == 'reject':
            friend_request.reject()
            return Response({'message': 'Запрос в друзья отклонен'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Недопустимое действие'}, status=status.HTTP_400_BAD_REQUEST)

class IncomingFriendRequestList(generics.ListAPIView):
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(to_user=user)

class OutgoingFriendRequestList(generics.ListAPIView):
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(from_user=user)

class FriendList(generics.ListAPIView):
    serializer_class = FriendSerializer

    def get_queryset(self):
        user = self.request.user
        return Friend.objects.filter(users=user)

class FriendshipStatus(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        other_user_id = request.GET.get('other_user_id')
        if not other_user_id:
            return Response({'error': 'other_user_id parameter is required'}, status=400)

        try:
            other_user = User.objects.get(id=other_user_id)
        except User.DoesNotExist:
            return Response({'error': 'Other user not found'}, status=404)

        friendship_status = user.get_friendship_status(other_user)
        return Response({'friendship_status': friendship_status})


class RemoveFriend(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        friend_id = self.kwargs['pk']
        try:
            friend = self.get_object()
            self.request.user.friends.remove(friend)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'error': 'Friend not found.'}, status=status.HTTP_404_NOT_FOUND)

class FriendRequestAction(APIView):
    def get(self, request, to_user, format=None):
        try:
            friend_request = FriendRequest.objects.filter(to_user=to_user)
            serializer = FriendRequestSerializer(friend_request, many=True)
            return Response(serializer.data)
        except FriendRequest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        from_user = request.data.get('from_user')
        to_user = request.data.get('to_user')
        if from_user and to_user:
            try:
                from_user = User.objects.get(id=from_user)
                return Response(status=status.HTTP_201_CREATED)
            except User.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)

