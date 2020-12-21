from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from django.http import HttpResponse, JsonResponse, HttpRequest
from .serializer import *
from .models import *
from .get_time import gettime
from datetime import timedelta
from typing import Dict, Any
from django.utils.datastructures import MultiValueDictKeyError

@api_view(['GET', ])
def get_all_room(request: HttpRequest) -> HttpResponse:
	datas = []
	if request.method == "GET":
		try:
			if request.query_params['order'] == "price":
				room = Room.objects.order_by('price')
			elif request.query_params['order'] == "price_desc":
				room = Room.objects.order_by('-price')
			elif request.query_params['order'] == "date":
				room = Room.objects.order_by('creation')
			elif request.query_params['order'] == "date_desc":
				room = Room.objects.order_by('-creation')
			else:
				return JsonResponse({'Сортировка': 'Указан неправильный параметр сортировки'}, \
															status=status.HTTP_400_BAD_REQUEST)
		except:
			room = Room.objects.all()
		for i in room:
			dicti = {}
			dicti['description'] = i.description
			dicti['price'] = i.price
			dicti['date_creation'] = i.creation
			datas.append(dicti)
		return Response(datas, status=status.HTTP_200_OK)

@api_view(['POST', ])
def room_add(request: HttpRequest) -> HttpResponse:
	if request.method == "POST":
		serializer = RoomSerializer(data=request.data)
		if serializer.is_valid():
			temp = Room(description=request.data['description'], price=request.data['price'])
			temp.save()
			return JsonResponse({'ID-номера': temp.id}, status=status.HTTP_201_CREATED)
		return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE', ])
def room_delete(request: HttpRequest, room_id: int) -> HttpResponse:
	if request.method == "DELETE":
		try:
			room = Room.objects.get(id=room_id)
			room.delete()
			return JsonResponse({'ID': 'Номер отеля с ID-{} был удален'.format(room_id)}, \
																status=status.HTTP_200_OK)
		except:
			return JsonResponse({'ID': 'Номер отеля с ID-{} не существует'.format(room_id)}, \
																status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', ])
def reserve_add(request: HttpRequest) -> HttpResponse:
	if request.method == "POST":
		serializer = ReserveSerializer(data=request.data)
		if serializer.is_valid():
			room_id = request.data['room_id']
			try:
				room = Room.objects.get(id=room_id)
			except:
				return JsonResponse({'ID': 'Номер отеля с ID-{} не существует'.format(room_id)}, \
																status=status.HTTP_400_BAD_REQUEST)
			date_start = gettime(request.data['date_start'])
			date_end = gettime(request.data['date_end'])
			if date_start > date_end:
				return Response('Дата окончания брони не может быть раньше даты начала брони', \
																status=status.HTTP_400_BAD_REQUEST)
			temp = Reserve(date_start=date_start, date_end=date_end, room=room)
			temp.save()
			return JsonResponse({'ID-брони': temp.id}, status=status.HTTP_201_CREATED)
		return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', ])
def get_all_reserve(request: HttpRequest) -> HttpResponse:
	datas = []
	if request.method == "GET":
		try:
			room_id = request.query_params['room_id']
			room = Room.objects.get(id=room_id)

		except MultiValueDictKeyError:
			return JsonResponse({'Параметр': 'Не указан параметр id номера'}, \
															status=status.HTTP_400_BAD_REQUEST)

		except Room.DoesNotExist:
			return JsonResponse({'ID': 'Номер отеля с ID-{} не существует'.format(room_id)}, \
																status=status.HTTP_400_BAD_REQUEST)

		except ValueError:
			return JsonResponse({'Тип': 'Введен неправильный формат данных'}, \
															status=status.HTTP_400_BAD_REQUEST)

		all_reserve = room.rm.order_by('date_start')
		for i in all_reserve:
			dicti = {}
			dicti['booking_id'] = i.id
			dicti['date_start'] = i.date_start
			dicti['date_end'] = i.date_end
			datas.append(dicti)
		return Response(datas, status=status.HTTP_200_OK)


@api_view(['DELETE', ])
def reserve_delete(request: HttpRequest, booking_id: int) -> HttpResponse:
	if request.method == "DELETE":
		try:
			reserve = Reserve.objects.get(id=booking_id)
			reserve.delete()
			return JsonResponse({'ID': 'Бронь с ID-{} был удален'.format(booking_id)}, \
																status=status.HTTP_200_OK)
		except:
			return JsonResponse({'ID': 'Бронь с ID-{} не существует'.format(booking_id)}, \
																status=status.HTTP_400_BAD_REQUEST)
