from rest_framework.routers import DefaultRouter
from .views import RoadmapViewSet

router = DefaultRouter()
router.register('', RoadmapViewSet, basename='roadmap')

urlpatterns = router.urls
