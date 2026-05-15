from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AIChatView, AIChatSessionViewSet, AIRoadmapView, AIRecommendationView, AICalculatorView

router = DefaultRouter()
router.register(r'sessions', AIChatSessionViewSet, basename='ai-session')

urlpatterns = [
    path('chat/', AIChatView.as_view(), name='ai-chat'),
    path('roadmap/', AIRoadmapView.as_view(), name='ai-roadmap'),
    path('recommend/', AIRecommendationView.as_view(), name='ai-recommend'),
    path('calculator/', AICalculatorView.as_view(), name='ai-calculator'),
    path('', include(router.urls)),
]