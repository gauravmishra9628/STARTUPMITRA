from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import AIChatSession, AIChatMessage, AIRecommendation
from .serializers import AIChatSessionSerializer, AIChatMessageSerializer, AIRecommendationSerializer
from .ai_service import ai_service


class AIChatView(APIView):
    """AI Chat API"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Send a message to AI chat"""
        message = request.data.get('message')
        mentor_type = request.data.get('mentor_type', 'general')
        language = request.data.get('language', 'en')
        session_id = request.data.get('session_id')

        if not message:
            return Response({'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)

        if session_id:
            session = AIChatSession.objects.filter(id=session_id, user=request.user).first()
        else:
            session = AIChatSession.objects.create(
                user=request.user,
                mentor_type=mentor_type,
                language=language
            )

        AIChatMessage.objects.create(session=session, sender='user', message=message)

        context = {'language': language}
        ai_response = ai_service.chat(message, mentor_type, language, context)

        AIChatMessage.objects.create(session=session, sender='ai', message=ai_response)

        return Response({
            'session_id': session.id,
            'response': ai_response,
            'timestamp': session.updated_at
        })


class AIChatSessionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for AI Chat Sessions"""
    serializer_class = AIChatSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AIChatSession.objects.filter(user=self.request.user)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """Get all messages in a session"""
        session = self.get_object()
        messages = session.messages.all()
        serializer = AIChatMessageSerializer(messages, many=True)
        return Response(serializer.data)


class AIRoadmapView(APIView):
    """AI Roadmap generation API"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Generate a business roadmap"""
        business_idea = request.data.get('business_idea')
        user_skills = request.data.get('skills', [])
        investment = request.data.get('investment', 0)
        language = request.data.get('language', 'en')

        if not business_idea:
            return Response({'error': 'Business idea is required'}, status=status.HTTP_400_BAD_REQUEST)

        roadmap = ai_service.generate_roadmap(business_idea, user_skills, float(investment), language)

        return Response({
            'roadmap': roadmap,
            'business_idea': business_idea
        })


class AIRecommendationView(APIView):
    """AI Recommendation API"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Get AI recommendations"""
        recommendation_type = request.data.get('type', 'business_ideas')
        user_budget = request.data.get('budget')
        user_skills = request.data.get('skills', [])
        interests = request.data.get('interests', [])
        language = request.data.get('language', 'en')

        recommendation_data = {
            'type': recommendation_type,
            'budget': user_budget,
            'skills': user_skills,
            'interests': interests,
            'generated_recommendations': []
        }

        AIRecommendation.objects.create(
            user=request.user,
            recommendation_type=recommendation_type,
            recommendation_data=recommendation_data
        )

        return Response(recommendation_data)


class AICalculatorView(APIView):
    """Investment Calculator API"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Calculate investment ROI"""
        investment = float(request.data.get('investment', 0))
        monthly_expenses = float(request.data.get('monthly_expenses', 0))
        expected_profit_percentage = float(request.data.get('profit_percentage', 20))
        months = int(request.data.get('months', 12))
        language = request.data.get('language', 'en')

        monthly_profit = (investment * expected_profit_percentage) / 100
        total_profit = monthly_profit * months
        total_expenses = monthly_expenses * months
        net_profit = total_profit - total_expenses
        roi = (net_profit / investment) * 100 if investment > 0 else 0

        return Response({
            'monthly_profit': round(monthly_profit, 2),
            'total_profit': round(total_profit, 2),
            'total_expenses': round(total_expenses, 2),
            'net_profit': round(net_profit, 2),
            'roi_percentage': round(roi, 2),
            'break_even_months': round(monthly_expenses / monthly_profit, 1) if monthly_profit > 0 else None
        })