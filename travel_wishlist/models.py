from django.db import models

# Create your models here.

class Place(models.Model): # import provided above, we will specify fields which will map to columns in a db
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)

    def __str__(self): # never displayed to the user but might be helpful for the developer to see
        return f'{self.name} visted? {self.visited}'

