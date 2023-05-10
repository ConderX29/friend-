from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

class User(AbstractBaseUser):
    username = models.CharField(max_length= 255, unique=True)
    password = models.CharField(max_length= 8)

    def get_friendship_status(self, other_user):
        friend_requests_sent = FriendRequest.objects.filter(from_user=self, to_user=other_user)
        friend_requests_received = FriendRequest.objects.filter(from_user=other_user, to_user=self)
        friends = Friend.objects.filter(users=self).filter(users=other_user)

        if friends.exists():
            return 'already_friends'
        elif friend_requests_sent.exists():
            return 'outgoing_request'
        elif friend_requests_received.exists():
            return 'incoming_request'
        else:
            return 'no_relationship'

    def remove_friend(self, friend):
        if self.is_friend(friend):
            self.friends.remove(friend)
            friend.friends.remove(self)

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='friend_requests_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='friend_requests_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    def accept(self):
        self.accepted = True
        Friend.objects.create(users=[self.from_user, self.to_user])
    def reject(self):
        self.delete()

class Friend(models.Model):
    sers = models.ManyToManyField(User, related_name='friendships')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.users.all()[0]} - {self.users.all()[1]}"

