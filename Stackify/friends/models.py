from django.db import models
from django.conf import settings

class FriendList(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='user')
    friends=models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='friends')

    def add_friend(self,account):
        if not account in FriendList.objects.all():
            self.friends.add(account)
            self.save()

    def unfriend(self,account):
        if account in FriendList.objects.all():
            self.friends.remove(account)
            self.save()

class FriendRequest(models.Model):
    sender=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='sender')
    reciever=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='reciever')
    is_active=models.BooleanField(blank=True,null=False,default=True)
    date=models.DateField(auto_now_add=True)

    def accept(self):
        reciever_friend_list=FriendList.objects.get(user=self.receiver)
        if reciever_friend_list:
            reciever_friend_list.add_friend(self.sender)
            sender_friend_list=FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.reciever)
                self.is_active=False
                self.save()

    def decline(self):
            self.is_active=False
            self.save()
    
    def cancel(self):
            self.is_active=False
            self.save()