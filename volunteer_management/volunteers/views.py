from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Volunteer
from .serializers import VolunteerSerializer

class VolunteerListView(APIView):
    def get(self, request):
        volunteers = Volunteer.objects.all()
        serializer = VolunteerSerializer(volunteers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VolunteerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VolunteerDetailView(APIView):
    """
    Handles retrieving, updating, and deleting a specific volunteer.
    """
    def get_object(self, pk):
        try:
            return Volunteer.objects.get(pk=pk)
        except Volunteer.DoesNotExist:
            return None

    def get(self, request, pk):
        volunteer = self.get_object(pk)
        if not volunteer:
            return Response({"error": "Volunteer not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = VolunteerSerializer(volunteer)
        return Response(serializer.data)

    def put(self, request, pk):
        volunteer = self.get_object(pk)
        if not volunteer:
            return Response({"error": "Volunteer not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = VolunteerSerializer(volunteer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        volunteer = self.get_object(pk)
        if not volunteer:
            return Response({"error": "Volunteer not found"}, status=status.HTTP_404_NOT_FOUND)
        volunteer.delete()
        return Response({"message": "Volunteer deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
