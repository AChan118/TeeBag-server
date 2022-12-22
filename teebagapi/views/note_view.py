from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from datetime import date
from teebagapi.models import Note
from teebagapi.models import Golfer

class NoteView(ViewSet):
    """Golf Notes"""

    def list(self, request):
        """Handle GET requests to notes resource

        Returns:
            Response -- JSON serialized list of notes
        """
        notes = Note.objects.all()

        serializer = NoteSerializer(
            notes, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single note

        Returns:
            Response -- JSON serialized note instance
        """

        note = Note.objects.get(pk=pk)
        serializer = NoteSerializer(note, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Note instance
        """
        golfer = Golfer.objects.get(user = request.auth.user)

        new_note = Note()
        new_note.title = request.data["title"]
        new_note.content = request.data["content"]
        new_note.date = date.today()
        new_note.golfer = golfer

        new_note.save()

        serializer = NoteSerializer(new_note, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests for a note

        Returns:
            Response -- Empty body with 204 status code
        """
        note = Note.objects.get(pk=pk)
        note.title = request.data["title"]
        note.content = request.data["content"]
        note.golfer = request.data["golfer"]
        note.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single note

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            note = Note.objects.get(pk=pk)
            note.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Note.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class NoteSerializer(serializers.ModelSerializer):
    """JSON serializer for notes

    Arguments:
        serializers
    """
    class Meta:
        model = Note
        fields = ('id', 'title', 'content', 'golfer')
        depth = 1