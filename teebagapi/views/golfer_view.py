from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from teebagapi.models import Golfer
from django.contrib.auth.models import User

class GolferView(ViewSet):
    def retrieve(self, request, pk):
        """Handle GET requests for single golfer

        Returns:
            Response -- JSON serialized golfer instance
        """

        if pk == "current":
            user = request.user
            golfer = Golfer.objects.get(user=user)
            data = {
                'username' : user.username,
                'firstName' : user.first_name,
                'lastName' : user.last_name,
                'email' : user.email,
                'isStaff' : user.is_staff,
                'isActive' : user.is_active,
                'bio' : golfer.bio,
                'profileImageUrl' : golfer.profile_image_url,
            }
            return Response(data, status=status.HTTP_200_OK)

        golfer = Golfer.objects.get(pk=pk)
        serializer = GolferSerializer(golfer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk):
        """Handle PUT requests for a golfer

        Returns:
            Response -- Empty body with 204 status code
        """
        golfer = Golfer.objects.get(pk=pk)
        user = User.objects.get(pk=golfer.user_id)

        user.username = request.data["username"]
        user.email = request.data["email"]
        user.is_active = request.data["isActive"]
        golfer.bio = request.data["bio"]
        golfer.profile_image_url = request.data["profileImageUrl"]
        user.save()
        golfer.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for golfers

    Arguments:
        serializers
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'is_staff', 'is_active')

class GolferSerializer(serializers.ModelSerializer):
    """JSON serializer for golfers

    Arguments:
        serializers
    """
    user = UserSerializer(many=False)
    class Meta:
        model = Golfer
        fields = ('id', "full_name", 'user', 'bio', 'profile_image_url')