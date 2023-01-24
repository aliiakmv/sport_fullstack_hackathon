from django.db.models import Count, Avg
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from applications.section.models import Section, Category
from applications.section.serializers import SectionSerializer


class RecommendationMixin:
    """Выводит топ 5 самых пролайканных курсов"""
    @action(detail=True, methods=['GET'])
    def get_recommended_courses(self, request):
        section = Section.objects.filter(id=request.data.get('pk')).get('category')
        print(section)
        #most_liked_courses = Section.objects.filter(category=section).annotate(total_likes=Count('likes')).order_by('likes')[:5]
        #courses = SectionSerializer(most_liked_courses, many=True)
        #return Response(courses.data, status.HTTP_200_OK)
