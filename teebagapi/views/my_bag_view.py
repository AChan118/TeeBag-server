from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from teebagapi.models import MyBag
from teebagapi.models import Golfer
from teebagapi.models import Club
from teebagapi.models import MyClub


class MyBagView(ViewSet):
    """Golf MyBags"""

    def list(self, request):
        """Handle GET requests to mybags resource

        Returns:
            Response -- JSON serialized list of mybags
        """
        mybags = MyBag.objects.all()
        golfer = self.request.query_params.get('golfer', None)
        if golfer is not None:
            mybags = mybags.filter(golfer__id=golfer)
            serializer = MyBagSerializer(
            mybags, many=True, context={'request': request})
            return Response(serializer.data)
        serializer = MyBagSerializer(
            mybags, many=True, context={'request': request
                                        })
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single mybag

        Returns:
            Response -- JSON serialized mybag instance
        """

        if pk == "current_bag":
            golfer = Golfer.objects.get(user=request.auth.user)
            golfer_bag = MyBag.objects.get(golfer=golfer)
        else:
            golfer_bag = MyBag.objects.get(pk=pk)


        
        serializer = MyBagSerializer(golfer_bag, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized MyBag instance
        """
        golfer = Golfer.objects.get(user=request.auth.user)

        new_mybag = MyBag()
        new_mybag.golfer = golfer

        new_mybag.save()

        serializer = MyBagSerializer(new_mybag, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests for a mybag

        Returns:
            Response -- Empty body with 204 status code
        """
        mybag = MyBag.objects.get(pk=pk)
        mybag.golfer = request.data["golfer"]

        mybag.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single mybag

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            mybag = MyBag.objects.get(pk=pk)
            mybag.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except MyBag.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ClubSerializer(serializers.ModelSerializer):
    """JSON serializer for clubs

    Arguments:
        serializers
    """
    class Meta:
        model = Club
        fields = ('id', 'name', 'image_url')

class MyClubSerializer(serializers.ModelSerializer):
    """JSON serializer for myclubs

    Arguments:
        serializers
    """
    club = ClubSerializer(many=False)

    class Meta:
        model = MyClub
        fields = ('id', 'club', 'brand', 'yardage', 'loft', 'club_note')

class MyBagSerializer(serializers.ModelSerializer):
    """JSON serializer for mybags

    Arguments:
        serializers
    """
    my_clubs = MyClubSerializer(many=True)

    class Meta:
        model = MyBag
        fields = ('id', 'golfer' , 'my_clubs')
        depth = 1
