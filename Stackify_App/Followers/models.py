from django.db import models
from django.conf import settings

class FollowList(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='user',unique="False")
    friends=models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='friends')

    def follow(self,acc):
       pass
    def unfollow(self,account):
        if account in FollowList.objects.all():
            self.friends.remove(account)
            self.save()
