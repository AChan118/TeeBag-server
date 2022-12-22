from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status

from teebagapi.models import Club

class ClubView(ViewSet):
    """Golf Clubs"""

    def list(self, request):
        """Handle GET requests to clubs resource

        Returns:
            Response -- JSON serialized list of clubs
        """
        clubs = Club.objects.all()

        serializer = ClubSerializer(
            clubs, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single club

        Returns:
            Response -- JSON serialized club instance
        """

        club = Club.objects.get(pk=pk)
        serializer = ClubSerializer(club, context={'request': request})
        return Response(serializer.data)

class ClubSerializer(serializers.ModelSerializer):
    """JSON serializer for golf clubs

    Arguments:
        serializers
    """
    class Meta:
        model = Club
        fields = ('id', 'name', 'image_url')
        depth = 1

    