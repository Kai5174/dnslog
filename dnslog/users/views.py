from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import IscanUserSerializer
from .models import User


# Create your views here.

def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'code':20000,
        'data':{
            'token': token
        }
    }

class UserInfo(APIView):
    permission_classes=[IsAuthenticated, ]

    def get(self, request):
        user = User.objects.get(username=request.user)
        ser = IscanUserSerializer(user)
        re_data = {
            "data": ser.data,
            "code": 20000,
            "message": "success"
        }
        return JsonResponse(re_data, safe=False)
    