from django.db import models
from base.models import User

def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)


# Create your models here.


class Annonce(models.Model):
  author = models.ForeignKey("base.user", related_name=("created_by"), on_delete=models.CASCADE)
  title = models.CharField(max_length=20,blank=True)
  description = models.TextField(null=False, blank=False)
  category = models.TextField(null=False, blank=False)
  theme = models.TextField(null=False, blank=False)
  sold = models.IntegerField(null=False, blank=False)
  wilaya = models.TextField(null=False, blank=False)
  commune = models.TextField(null=False, blank=False)
  created = models.DateTimeField(auto_now_add=True)
  surface= models.FloatField(null=False, blank=False)


  def __str__(self):
        return self.title

class Photo(models.Model):
    owner = models.ForeignKey("annonce", related_name=("images"), on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to,  null = True , blank = True)



class Adress(models.Model):
    wilaya = models.CharField(max_length=20,blank=True, null = True)
    commune = models.CharField(max_length=20,blank=True, null = True)


    def __str__(self):
        return self.commune + " " +self.wilaya
    
class Fav(models.Model):
    user  = models.ForeignKey("base.user", related_name=("person"), on_delete=models.CASCADE)
    annonce  = models.ForeignKey("annonce", related_name=("Annonce"), on_delete=models.CASCADE)

    class Meta:
       unique_together = ("user", "annonce")


