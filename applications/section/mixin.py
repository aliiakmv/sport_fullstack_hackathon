from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from applications.section.models import Section
from applications.section.serializers import SectionSerializer


class RecommendationsMixin:
    @action(detail=False, methods=['GET'])
    def get_recommendations(self, request):
        most_liked_gyms = Section.objectss.order_by('ratings')[:10]
        serializer = SectionSerializer(most_liked_gyms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
