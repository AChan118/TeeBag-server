from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from teebagapi.models import Round
from teebagapi.models import Hole
from teebagapi.models import Golfer
from teebagapi.models import Course

class RoundView(ViewSet):
    """Golf Rounds"""

    def list(self, request):
        """Handle GET requests to rounds resource

        Returns:
            Response -- JSON serialized list of rounds
        """

        rounds = Round.objects.all()
        golfer = self.request.query_params.get('golfer', None)
        recent= self.request.query_params.get('recent', None)
        if golfer is not None:
            rounds = rounds.filter(golfer__id=golfer)
            sorted_rounds = sorted(rounds, key=lambda round: round.date, reverse=True)
            serializer = RoundSerializer(
            sorted_rounds, many=True, context={'request': request})
            return Response(serializer.data)
        elif recent is not None:
            rounds = rounds.filter(golfer__id=recent)
            sorted_rounds = sorted(rounds, key=lambda round: round.date, reverse=True)
            serializer = RoundSerializer(
            sorted_rounds[:5], many=True, context={'request': request})
            return Response(serializer.data)
            
        serializer = RoundSerializer(
            rounds, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single round

        Returns:
            Response -- JSON serialized round instance
        """

        round = Round.objects.get(pk=pk)
        serializer = RoundSerializer(round, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Round instance
        """
        golfer = Golfer.objects.get(user = request.auth.user)
        course = Course.objects.get(pk=request.data["course"])

        new_round = Round()
        new_round.date = request.data["date"]
        new_round.golfer = golfer
        new_round.course = course
        new_round.is_full_round = request.data["isFullRound"]

        new_round.save()

        serializer = RoundSerializer(new_round, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests for a round

        Returns:
            Response -- Empty body with 204 status code
        """
        round = Round.objects.get(pk=pk)
        round.date = request.data["date"]
        round.golfer = request.data["golfer"]
        round.course = request.data["course"]
        round.is_full_round = request.data["isFullRound"]
        round.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single round

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            round = Round.objects.get(pk=pk)
            round.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Round.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RoundCourseSerializer(serializers.ModelSerializer):
    """JSON serializer for rounds

    Arguments:
        serializers
    """
    class Meta:
        model = Course
        fields = ('id', 'name', 'total_par')
 

class HoleSerializer(serializers.ModelSerializer):
    """JSON serializer for holes

    Arguments:
        serializers
    """
    class Meta:
        model = Hole
        fields = ('id', 'round', 'score')
        depth = 1
class RoundSerializer(serializers.ModelSerializer):
    """JSON serializer for rounds

    Arguments:
        serializers
    """
    course = RoundCourseSerializer(many=False)

    class Meta:
        model = Round
        fields = ('id', 'date', 'golfer', 'course', 'is_full_round')
        
  