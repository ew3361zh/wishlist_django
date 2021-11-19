from django.contrib import admin
# import new Place model:
from .models import Place, CatFact

# register that model with the admin console
admin.site.register(Place)
admin.site.register(CatFact)

# Register your models here.
