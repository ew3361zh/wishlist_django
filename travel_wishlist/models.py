from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage

# Create your models here.

class CatFact(models.Model):
    fact = models.CharField(max_length=500)

    def __str__(self):
        return self.fact


class Place(models.Model): # import provided above, we will specify fields which will map to columns in a db
    user = models.ForeignKey('auth.User', null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    date_visited = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True)


    def save(self, *args, **kwargs):
        old_place = Place.objects.filter(pk=self.pk).first()
        if old_place and old_place.photo:
            if old_place.photo != self.photo:
                self.delete_photo(old_place.photo)
        # if there is an old place, and that old place has a photo, and that photo is different than the new photo, delete that old photo
        super().save(*args, **kwargs) 

    def delete_photo(self, photo):
        if default_storage.exists(photo.name):
            default_storage.delete(photo.name)
    

    def delete(self, *args, **kwargs):
        if self.photo:
            self.delete_photo(self.photo)
        
        super().delete(*args, **kwargs)

    def __str__(self): # never displayed to the user but might be helpful for the developer to see
        photo_str = self.photo.url if self.photo else 'no photo'
        notes_str = self.notes[100:] if self.notes else 'no notes'
        return f'{self.name} visted? {self.visited} on {self.date_visited}. Notes: {notes_str}. Photo {photo_str}'

