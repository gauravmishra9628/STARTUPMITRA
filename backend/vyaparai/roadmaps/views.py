from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Roadmap
from .serializers import RoadmapSerializer
from django.db.models import Q


class RoadmapViewSet(viewsets.ModelViewSet):
    serializer_class = RoadmapSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # users see their own roadmaps; public roadmaps are visible to all
        user = self.request.user
        return Roadmap.objects.filter(Q(user=user) | Q(is_public=True))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def duplicate(self, request, pk=None):
        roadmap = self.get_object()
        roadmap.pk = None
        roadmap.user = request.user
        roadmap.is_public = False
        roadmap.save()
        return Response(RoadmapSerializer(roadmap).data)
