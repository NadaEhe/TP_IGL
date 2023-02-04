from django.contrib import admin

# Register your models here.

from .models import Annonce , Adress  , Fav , Photo


admin.site.register(Annonce)
admin.site.register(Adress)
admin.site.register(Fav)
admin.site.register(Photo)
