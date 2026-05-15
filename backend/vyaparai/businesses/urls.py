from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, BusinessIdeaViewSet, SavedBusinessViewSet, BusinessRoadmapViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'ideas', BusinessIdeaViewSet, basename='business-idea')
router.register(r'saved', SavedBusinessViewSet, basename='saved-business')
router.register(r'roadmaps', BusinessRoadmapViewSet, basename='roadmap')

urlpatterns = [
    path('', include(router.urls)),
]