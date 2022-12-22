from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from teebagapi.models import Hole
from teebagapi.models import Round

class HoleView(ViewSet):
    """Golf Holes"""

    def list(self, request):
        """Handle GET requests to holes resource

        Returns:
            Response -- JSON serialized list of holes
        """
        holes = Hole.objects.all()
        
        round = self.request.query_params.get('round', None)
        if round is not None:
            holes = holes.filter(round__id=round)
            serializer = HoleSerializer(
            holes, many=True, context={'request': request})
            return Response(serializer.data)


        serializer = HoleSerializer(
            holes, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single hole

        Returns:
            Response -- JSON serialized hole instance
        """

        hole = Hole.objects.get(pk=pk)
        serializer = HoleSerializer(hole, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Hole instance
        """
        round = Round.objects.get(pk=request.data["round"])

        new_hole = Hole()
        new_hole.score = request.data["score"]
        new_hole.round = round

        new_hole.save()

        serializer = HoleSerializer(new_hole, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests for a hole

        Returns:
            Response -- Empty body with 204 status code
        """
        round = Round.objects.get(pk=request.data["round"])

        hole = Hole.objects.get(pk=pk)
        hole.score = request.data["score"]
        hole.round = round
        hole.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    

class HoleSerializer(serializers.ModelSerializer):
    """JSON serializer for holes

    Arguments:
        serializers
    """
    class Meta:
        model = Hole
        fields = ('id', 'score', 'round')
        depth = 2