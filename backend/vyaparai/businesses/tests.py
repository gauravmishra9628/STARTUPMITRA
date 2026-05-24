from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import BusinessIdea, Category, SavedBusiness


User = get_user_model()


class BusinessApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='bizfounder',
            email='bizfounder@example.com',
            password='StrongPass123!',
        )
        self.category = Category.objects.create(
            name='Food & Beverage',
            name_hi='खाद्य एवं पेय',
            icon='🍔',
            description='Food ideas',
            description_hi='खाद्य विचार',
        )
        self.idea = BusinessIdea.objects.create(
            title='Cloud Kitchen Starter',
            title_hi='क्लाउड किचन स्टार्टर',
            description='Delivery-first cloud kitchen model.',
            description_hi='डिलीवरी-फर्स्ट क्लाउड किचन मॉडल।',
            category=self.category,
            min_investment=150000,
            max_investment=300000,
            estimated_profit=90000,
            profit_percentage=30,
            difficulty='medium',
            skills_required=['operations', 'marketing'],
            market_demand=80,
            risk_level=40,
        )

    def test_business_list_and_save(self):
        list_response = self.client.get('/api/businesses/ideas/')
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(list_response.data['count'], 1)

        self.client.force_authenticate(user=self.user)
        save_response = self.client.post(f'/api/businesses/ideas/{self.idea.id}/save/')
        self.assertEqual(save_response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(SavedBusiness.objects.filter(user=self.user, business=self.idea).exists())
