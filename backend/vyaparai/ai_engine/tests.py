from unittest.mock import patch

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import AIChatMessage, AIChatSession, AIRecommendation


User = get_user_model()


class AIEngineApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='aifounder',
            email='aifounder@example.com',
            password='StrongPass123!',
        )

    @patch('ai_engine.views.ai_service.chat', return_value='Mocked mentor response')
    def test_chat_creates_session_and_message(self, mocked_chat):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            '/api/ai/chat/',
            {'message': 'Best business under ₹50,000?', 'mentor_type': 'general', 'language': 'en'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['session_id'])
        self.assertEqual(AIChatSession.objects.filter(user=self.user).count(), 1)
        self.assertEqual(AIChatMessage.objects.filter(session__user=self.user).count(), 2)
        mocked_chat.assert_called_once()

    @patch('ai_engine.views.ai_service.generate_roadmap')
    def test_roadmap_generation(self, mocked_generate_roadmap):
        mocked_generate_roadmap.return_value = {
            'phases': [],
            'total_duration': '3 months',
            'risk_mitigation': [],
            'success_metrics': [],
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            '/api/ai/roadmap/',
            {'business_idea': 'Cloud kitchen', 'skills': ['marketing'], 'investment': 200000, 'language': 'en'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['business_idea'], 'Cloud kitchen')
        mocked_generate_roadmap.assert_called_once()

    @patch('ai_engine.views.ai_service.generate_recommendations')
    def test_recommendations_generation(self, mocked_generate_recommendations):
        mocked_generate_recommendations.return_value = {
            'recommendations': [{'title': 'Micro SaaS', 'category': 'Tech'}],
            'insights': ['Start lean'],
            'next_steps': ['Validate demand'],
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            '/api/ai/recommend/',
            {'type': 'business_ideas', 'budget': '₹50000', 'skills': ['sales'], 'interests': ['tech'], 'language': 'en'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(AIRecommendation.objects.filter(user=self.user).exists())
        self.assertIn('recommendations', response.data)
        mocked_generate_recommendations.assert_called_once()
