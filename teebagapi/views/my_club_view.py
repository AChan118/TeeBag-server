from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from teebagapi.models import MyClub
from teebagapi.models import Golfer
from teebagapi.models import Club

class MyClubView(ViewSet):
    """Golf MyClubs"""

    def list(self, request):
        """Handle GET requests to myclubs resource

        Returns:
            Response -- JSON serialized list of myclubs
        """
        myclubs = MyClub.objects.all()

        serializer = MyClubSerializer(
            myclubs, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single myclub

        Returns:
            Response -- JSON serialized myclub instance
        """

        myclub = MyClub.objects.get(pk=pk)
        serializer = MyClubSerializer(myclub, context={'request': request})
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized MyClub instance
        """
        golfer = Golfer.objects.get(user = request.auth.user)
        club = Club.objects.get(pk=request.data["club"])

        new_myclub = MyClub()
        brand = request.data["brand"]
        yardage = request.data["yardage"]
        loft = request.data["loft"]
        club_notes = request.data["clubNotes"]
        new_myclub.golfer = golfer
        new_myclub.club = club

        new_myclub.save()

        serializer = MyClubSerializer(new_myclub, context={'request': request})

        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single myclub

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            myclub = MyClub.objects.get(pk=pk)
            myclub.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except MyClub.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def update(self, request, pk=None):
        """Handle PUT requests for a myclub

        Returns:
            Response -- Empty body with 204 status code
        """
        golfer = Golfer.objects.get(user = request.auth.user)
        club = Club.objects.get(pk=request.data["club"])

        myclub = MyClub.objects.get(pk=pk)
        myclub.golfer = golfer
        myclub.club = club
        myclub.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
class MyClubSerializer(serializers.ModelSerializer):
    """JSON serializer for myclubs

    Arguments:
        serializers
    """
    class Meta:
        model = MyClub
        fields = ('id', 'golfer', 'club', 'brand', 'yardage', 'loft', 'club_note')
        depth = 1
        