from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import DNSLog
from datetime import timedelta
from django.utils import timezone
from django.http import JsonResponse
import socketserver
import struct
import socket as socketlib
# Create your views here.


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'code':20000,
        'data':{
            'token': token
        }
    }

def success(data):
    return {
        'code': 20000,
        'data': data
    }

class Verify(APIView):
    permission_classes=[IsAuthenticated, ]

    def get(self, request):
        query = request.GET['q']
        last_date = timezone.now().date() - timedelta(days=1)
        rec_log = DNSLog.objects.filter(created_at__gte=last_date).filter(content=query)
        if len(rec_log) != 0:
            return JsonResponse(success('Yes'), safe=False)
        else:
            return JsonResponse(success('No'), safe=False)



