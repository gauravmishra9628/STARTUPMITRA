"""
AI Service for OpenAI and Gemini integration
"""
import os
import logging
from typing import Optional

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

            system_prompt = self._get_mentor_prompt(mentor_type, language)
            messages = [
                {'role': 'system', 'content': system_prompt}
            ]

            if context:
                messages.append({'role': 'system', 'content': f"Context: {context}"})

            messages.append({'role': 'user', 'content': message})

            response = client.chat.completions.create(
                model='gpt-4',
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

            model = genai.GenerativeModel('gemini-pro')
            system_prompt = self._get_mentor_prompt(mentor_type, language)

            prompt = f"{system_prompt}\n\nUser: {message}"
            if context:
                prompt += f"\nContext: {context}"

            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini error: {str(e)}")
            return self._fallback_response(message, mentor_type, language)

    def _get_mentor_prompt(self, mentor_type: str, language: str) -> str:
        """Get system prompt based on mentor type and language"""
        language_note = "Respond in Hindi" if language == 'hi' else "Respond in English"

        prompts = {
            'startup_strategist': f"You are a Startup Strategist expert. {language_note} Help users with business planning, market analysis, and startup strategies. Provide practical, actionable advice.",
            'financial_advisor': f"You are a Financial Advisor expert. {language_note} Help users with investment analysis, ROI calculations, profit estimation, and financial planning.",
            'marketing_guru': f"You are a Marketing Guru expert. {language_note} Help users with growth hacking, marketing strategies, customer acquisition, and brand building.",
            'tech_architect': f"You are a Tech Architect expert. {language_note} Help users with technical planning, technology stacks, and implementation strategies.",
            'general': f"You are a helpful business AI assistant for VyaparAI. {language_note} Help entrepreneurs with business ideas, startup guidance, and growth strategies.",
        }

        return prompts.get(mentor_type, prompts['general'])

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

        prompt = f"""Generate a detailed business roadmap for: {business_idea}
User skills: {', '.join(user_skills)}
Available investment: ₹{investment}
Language: {'Hindi' if language == 'hi' else 'English'}

Provide a JSON response with:
- phases: array of phases with title, duration, tasks, and key_milestones
- total_duration: estimated months
- risk_mitigation: array of potential risks and mitigations
- success_metrics: key metrics to track"""

        response = client.chat.completions.create(
            model='gpt-4',
            messages=[{'role': 'user', 'content': prompt}],
            max_tokens=2000,
            temperature=0.7
        )

        import json
        try:
            return json.loads(response.choices[0].message.content)
        except:
            return self._fallback_roadmap(business_idea, user_skills, investment, language)

    def _gemini_roadmap(self, business_idea: str, user_skills: list, investment: float, language: str) -> dict:
        """Generate roadmap using Gemini"""
        import google.generativeai as genai
        genai.configure(api_key=self.gemini_api_key)

        model = genai.GenerativeModel('gemini-pro')

        prompt = f"""Generate a detailed business roadmap for: {business_idea}
User skills: {', '.join(user_skills)}
Available investment: ₹{investment}
Language: {'Hindi' if language == 'hi' else 'English'}

Provide a JSON response with:
- phases: array of phases with title, duration, tasks, and key_milestones
- total_duration: estimated months
- risk_mitigation: array of potential risks and mitigations
- success_metrics: key metrics to track"""

        response = model.generate_content(prompt)
        import json
        try:
            return json.loads(response.text)
        except:
            return self._fallback_roadmap(business_idea, user_skills, investment, language)

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