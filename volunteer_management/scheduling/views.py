from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Participation
from .serializers import ParticipationSerializer

class ParticipationListView(APIView):
    def get(self, request):
        participations = Participation.objects.all()
        serializer = ParticipationSerializer(participations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ParticipationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
