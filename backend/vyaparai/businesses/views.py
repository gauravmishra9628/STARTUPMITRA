from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Category, BusinessIdea, SavedBusiness, BusinessRoadmap
from .serializers import (
    CategorySerializer, BusinessIdeaSerializer, BusinessIdeaListSerializer,
    SavedBusinessSerializer, BusinessRoadmapSerializer
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Categories"""
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class BusinessIdeaViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Business Ideas"""
    queryset = BusinessIdea.objects.all().select_related('category')
    serializer_class = BusinessIdeaListSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BusinessIdeaSerializer
        return BusinessIdeaListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        category = self.request.query_params.get('category')
        difficulty = self.request.query_params.get('difficulty')
        min_investment = self.request.query_params.get('min_investment')
        max_investment = self.request.query_params.get('max_investment')
        search = self.request.query_params.get('search')
        language = self.request.query_params.get('language', 'en')

        if category:
            queryset = queryset.filter(category_id=category)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        if min_investment:
            queryset = queryset.filter(min_investment__gte=min_investment)
        if max_investment:
            queryset = queryset.filter(max_investment__lte=max_investment)
        if search:
            if language == 'hi':
                queryset = queryset.filter(Q(title_hi__icontains=search) | Q(description_hi__icontains=search))
            else:
                queryset = queryset.filter(Q(title__icontains=search) | Q(description__icontains=search))

        return queryset

    @action(detail=True, methods=['post'])
    def save(self, request, pk=None):
        """Save a business idea"""
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

        business = self.get_object()
        saved, created = SavedBusiness.objects.get_or_create(user=request.user, business=business)

        if created:
            return Response({'message': 'Business saved successfully'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Already saved'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'])
    def unsave(self, request, pk=None):
        """Unsave a business idea"""
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

        business = self.get_object()
        try:
            saved = SavedBusiness.objects.get(user=request.user, business=business)
            saved.delete()
            return Response({'message': 'Business unsaved successfully'}, status=status.HTTP_204_NO_CONTENT)
        except SavedBusiness.DoesNotExist:
            return Response({'error': 'Business not saved'}, status=status.HTTP_404_NOT_FOUND)


class SavedBusinessViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for user's saved businesses"""
    serializer_class = SavedBusinessSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavedBusiness.objects.filter(user=self.request.user).select_related('business__category')


class BusinessRoadmapViewSet(viewsets.ModelViewSet):
    """ViewSet for Business Roadmaps"""
    serializer_class = BusinessRoadmapSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BusinessRoadmap.objects.filter(user=self.request.user).select_related('business')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)