from django.contrib import admin
# import new Place model:
from .models import Place

# register that model with the admin console
admin.site.register(Place)

# Register your models here.
