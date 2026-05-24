"""
AI Service for OpenAI and Gemini integration
"""
import os
import logging
import json
import re
from typing import Optional

from .prompt_templates import PromptTemplates

logger = logging.getLogger(__name__)


class AIService:
    """Service for handling AI API calls"""

    def __init__(self):
        self.openai_api_key = os.environ.get('OPENAI_API_KEY', '')
        self.gemini_api_key = os.environ.get('GEMINI_API_KEY', '')
        self.preferred_model = os.environ.get('AI_MODEL', 'openai')

    def chat(self, message: str, mentor_type: str = 'general', language: str = 'en', context: Optional[dict] = None) -> str:
        """Generate AI chat response"""
        try:
            if self.preferred_model == 'gemini' and self.gemini_api_key:
                return self._gemini_chat(message, mentor_type, language, context)
            elif self.openai_api_key:
                return self._openai_chat(message, mentor_type, language, context)
            else:
                return self._fallback_response(message, mentor_type, language)
        except Exception as e:
            logger.error(f"AI chat error: {str(e)}")
            return self._fallback_response(message, mentor_type, language)

    def _openai_chat(self, message: str, mentor_type: str, language: str, context: Optional[dict]) -> str:
        """OpenAI GPT chat"""
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.openai_api_key)

            system_prompt = PromptTemplates.mentor_system_prompt(mentor_type, language, context)
            messages = [{'role': 'system', 'content': system_prompt}]

            if context:
                messages.append({'role': 'system', 'content': f"Extra context: {context}"})

            messages.append({'role': 'user', 'content': message})

            response = client.chat.completions.create(
                model=os.environ.get('OPENAI_MODEL', 'gpt-4o-mini'),
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )

            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI error: {str(e)}")
            return self._fallback_response(message, mentor_type, language)

    def _gemini_chat(self, message: str, mentor_type: str, language: str, context: Optional[dict]) -> str:
        """Google Gemini chat"""
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.gemini_api_key)

            model = genai.GenerativeModel(os.environ.get('GEMINI_MODEL', 'gemini-1.5-flash'))
            system_prompt = PromptTemplates.mentor_system_prompt(mentor_type, language, context)

            prompt = f"{system_prompt}\n\nUser: {message}"

            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini error: {str(e)}")
            return self._fallback_response(message, mentor_type, language)

    def _fallback_response(self, message: str, mentor_type: str, language: str) -> str:
        """Fallback response when AI is unavailable"""
        if language == 'hi':
            return "मैं वर्तमान में अपनी क्षमताओं को बढ़ा रहा हूं। कृपया अपना प्रश्न फिर से पूछें।"
        return "I'm currently expanding my capabilities. Please try again or rephrase your question."

    def generate_roadmap(self, business_idea: str, user_skills: list, investment: float, language: str = 'en') -> dict:
        """Generate business roadmap"""
        try:
            if self.preferred_model == 'gemini' and self.gemini_api_key:
                return self._gemini_roadmap(business_idea, user_skills, investment, language)
            elif self.openai_api_key:
                return self._openai_roadmap(business_idea, user_skills, investment, language)
            else:
                return self._fallback_roadmap(business_idea, user_skills, investment, language)
        except Exception as e:
            logger.error(f"Roadmap generation error: {str(e)}")
            return self._fallback_roadmap(business_idea, user_skills, investment, language)

    def _openai_roadmap(self, business_idea: str, user_skills: list, investment: float, language: str) -> dict:
        """Generate roadmap using OpenAI"""
        from openai import OpenAI
        client = OpenAI(api_key=self.openai_api_key)

        prompt = PromptTemplates.roadmap_prompt(business_idea, user_skills, investment, language)

        response = client.chat.completions.create(
            model=os.environ.get('OPENAI_MODEL', 'gpt-4o-mini'),
            messages=[{'role': 'user', 'content': prompt}],
            max_tokens=2000,
            temperature=0.7
        )

        try:
            return self._parse_json_response(response.choices[0].message.content)
        except Exception:
            return self._fallback_roadmap(business_idea, user_skills, investment, language)

    def _gemini_roadmap(self, business_idea: str, user_skills: list, investment: float, language: str) -> dict:
        """Generate roadmap using Gemini"""
        import google.generativeai as genai
        genai.configure(api_key=self.gemini_api_key)

        model = genai.GenerativeModel(os.environ.get('GEMINI_MODEL', 'gemini-1.5-flash'))

        prompt = PromptTemplates.roadmap_prompt(business_idea, user_skills, investment, language)

        response = model.generate_content(prompt)
        try:
            return self._parse_json_response(response.text)
        except Exception:
            return self._fallback_roadmap(business_idea, user_skills, investment, language)

    def generate_recommendations(self, recommendation_type: str, budget: str | None, skills: list, interests: list, language: str = 'en') -> dict:
        """Generate recommendation payloads for business discovery."""
        try:
            if self.preferred_model == 'gemini' and self.gemini_api_key:
                return self._gemini_recommendations(recommendation_type, budget, skills, interests, language)
            if self.openai_api_key:
                return self._openai_recommendations(recommendation_type, budget, skills, interests, language)
            return self._fallback_recommendations(recommendation_type, budget, skills, interests, language)
        except Exception as e:
            logger.error(f"Recommendation generation error: {str(e)}")
            return self._fallback_recommendations(recommendation_type, budget, skills, interests, language)

    def _openai_recommendations(self, recommendation_type: str, budget: str | None, skills: list, interests: list, language: str) -> dict:
        from openai import OpenAI

        client = OpenAI(api_key=self.openai_api_key)
        prompt = PromptTemplates.recommendation_prompt(recommendation_type, budget, skills, interests, language)

        response = client.chat.completions.create(
            model=os.environ.get('OPENAI_MODEL', 'gpt-4o-mini'),
            messages=[{'role': 'user', 'content': prompt}],
            max_tokens=1800,
            temperature=0.6,
        )

        try:
            return self._parse_json_response(response.choices[0].message.content)
        except Exception:
            return self._fallback_recommendations(recommendation_type, budget, skills, interests, language)

    def _gemini_recommendations(self, recommendation_type: str, budget: str | None, skills: list, interests: list, language: str) -> dict:
        import google.generativeai as genai

        genai.configure(api_key=self.gemini_api_key)
        model = genai.GenerativeModel(os.environ.get('GEMINI_MODEL', 'gemini-1.5-flash'))
        prompt = PromptTemplates.recommendation_prompt(recommendation_type, budget, skills, interests, language)

        response = model.generate_content(prompt)

        try:
            return self._parse_json_response(response.text)
        except Exception:
            return self._fallback_recommendations(recommendation_type, budget, skills, interests, language)

    def _fallback_recommendations(self, recommendation_type: str, budget: str | None, skills: list, interests: list, language: str) -> dict:
        return {
            'recommendations': [
                {
                    'title': 'Cloud Kitchen Starter',
                    'category': 'Food & Beverage',
                    'estimated_investment': budget or '₹3L-₹5L',
                    'expected_profit': '25-40% ROI',
                    'difficulty': 'Intermediate',
                    'reason': 'Low physical footprint and strong local demand.',
                },
                {
                    'title': 'Micro SaaS Lead Tool',
                    'category': 'Tech & SaaS',
                    'estimated_investment': budget or '₹1L-₹2L',
                    'expected_profit': '35-55% ROI',
                    'difficulty': 'Beginner',
                    'reason': 'Can be launched lean with subscription revenue.',
                },
            ],
            'insights': [
                'Validate demand with 10-20 customer interviews.',
                'Start with one channel before expanding marketing spend.',
            ],
            'next_steps': [
                'Shortlist 3 ideas that fit your skills.',
                'Estimate monthly burn and break-even point.',
                'Create a 30-day pilot plan.',
            ],
        }

    def _parse_json_response(self, raw_content: str) -> dict:
        """Parse model output that may include code fences or leading text."""
        cleaned = raw_content.strip()
        cleaned = re.sub(r'^```(?:json)?\s*', '', cleaned)
        cleaned = re.sub(r'\s*```$', '', cleaned)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            start = cleaned.find('{')
            end = cleaned.rfind('}')
            if start != -1 and end != -1 and end > start:
                return json.loads(cleaned[start:end + 1])
            raise

    def _fallback_roadmap(self, business_idea: str, user_skills: list, investment: float, language: str) -> dict:
        """Fallback roadmap"""
        return {
            'phases': [
                {
                    'title': 'Phase 1: Planning' if language == 'hi' else 'Phase 1: Planning',
                    'duration': '1-2 months',
                    'tasks': ['Market research', 'Business model creation', 'Financial planning'],
                    'key_milestones': ['Business plan ready', 'Initial funding secured']
                },
                {
                    'title': 'Phase 2: Setup' if language == 'hi' else 'Phase 2: Setup',
                    'duration': '2-3 months',
                    'tasks': ['Legal registration', 'Infrastructure setup', 'Team building'],
                    'key_milestones': ['Company registered', 'Office/facility ready']
                },
                {
                    'title': 'Phase 3: Launch' if language == 'hi' else 'Phase 3: Launch',
                    'duration': '1-2 months',
                    'tasks': ['Marketing campaign', 'Soft launch', 'Customer acquisition'],
                    'key_milestones': ['First customers', 'Initial revenue']
                }
            ],
            'total_duration': '5-7 months',
            'risk_mitigation': [
                {'risk': 'Market uncertainty', 'mitigation': 'Start with minimum viable product'},
                {'risk': 'Cash flow issues', 'mitigation': 'Maintain 3-month runway'}
            ],
            'success_metrics': ['Monthly revenue growth', 'Customer acquisition cost', 'Customer retention rate']
        }


ai_service = AIService()