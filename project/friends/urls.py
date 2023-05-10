from django.urls import path
from .views import UserRegistration
from .views import FriendRequestList
from .views import FriendRequestDetail
from .views import IncomingFriendRequestList, OutgoingFriendRequestList
from .views import FriendList
from .views import FriendshipStatus
from .views import RemoveFriend

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user-registration'),
    path('friend-requests/', FriendRequestList.as_view(), name='friend_request_list'),
    path('friend-requests/<int:pk>/', FriendRequestDetail.as_view(), name='friend_request_detail'),
    path('friend-requests/incoming/', IncomingFriendRequestList.as_view(), name='incoming-friend-requests'),
    path('friend-requests/outgoing/', OutgoingFriendRequestList.as_view(), name='outgoing-friend-requests'),
    path('friends/', FriendList.as_view(), name='friend-list'),
    path('friendship-status/<int:user_id>/', FriendshipStatus.as_view(), name='friendship-status'),
    path('remove_friend/<int:pk>/', RemoveFriend.as_view(), name='remove_friend'),
]