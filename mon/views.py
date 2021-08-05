from mon.serializers import TestMonSerializers
from mon.models import TestMongo
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics


class TestQuery(APIView):
    def get(self, request):
        return Response(data={'message': 'hello world', }, status=status.HTTP_202_ACCEPTED)


class AllTestMon(generics.ListAPIView):
    queryset = TestMongo.objects.all()
    serializer_class = TestMonSerializers
