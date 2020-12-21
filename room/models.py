from django.db import models


class Room(models.Model):
	description = models.CharField(max_length=200)
	price = models.IntegerField(db_index=True)
	creation = models.DateField(auto_now_add=True)

class Reserve(models.Model):
	date_start = models.DateField(db_index=True)
	date_end = models.DateField()
	room = models.ForeignKey(Room, on_delete = models.CASCADE, related_name='rm')
# Create your models here.
