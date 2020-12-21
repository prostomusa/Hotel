from rest_framework import serializers

from .models import *

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['description', 'price']

class ReserveSerializer(serializers.ModelSerializer):
	room_id = serializers.IntegerField()
	class Meta:
		model = Reserve
		fields = ['room_id', 'date_start', 'date_end']