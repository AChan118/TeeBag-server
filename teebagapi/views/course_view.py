from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from teebagapi.models import Course


class CourseView(ViewSet):
    """Golf Courses"""

    def list(self, request):
        """Handle GET requests to courses resource

        Returns:
            Response -- JSON serialized list of courses
        """
        courses = Course.objects.all()

        serializer = CourseSerializer(
            courses, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single course

        Returns:
            Response -- JSON serialized course instance
        """

        course = Course.objects.get(pk=pk)
        serializer = CourseSerializer(course, context={'request': request})
        return Response(serializer.data)


    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Course instance
        """
        new_course = Course()
        new_course.name = request.data["name"]
        new_course.city = request.data["city"]
        new_course.state = request.data["state"]
        new_course.front_nine_par = request.data["frontNinePar"]
        new_course.back_nine_par = request.data["backNinePar"]
        
        new_course.save()

        serializer = CourseSerializer(new_course, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests for a course

        Returns:
            Response -- Empty body with 204 status code
        """
        course = Course.objects.get(pk=pk)
        course.name = request.data["name"]
        course.city = request.data["city"]
        course.state = request.data["state"]
        course.front_nine_par = request.data["frontNinePar"]
        course.back_nine_par = request.data["backNinePar"]
        course.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single course

        Returns:
            Response -- 200, 404, or 500 status code
        """
        
        course = Course.objects.get(pk=pk)
        course.delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

class CourseSerializer(serializers.ModelSerializer):
    """JSON serializer for courses

    Arguments:
        serializers
    """
    class Meta:
        model = Course
        fields = ('id', 'name', 'city', 'state', 'front_nine_par', 'back_nine_par', 'total_par' )

