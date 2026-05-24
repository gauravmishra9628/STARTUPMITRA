"""Reusable AI prompt templates for VyaparAI."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PromptTemplates:
    """Central prompt templates used by the AI service."""

    @staticmethod
    def language_note(language: str) -> str:
        return "Respond in Hindi. Use simple, natural Hindi." if language == 'hi' else "Respond in English. Use clear, concise business language."

    @staticmethod
    def mentor_system_prompt(mentor_type: str, language: str, context: dict | None = None) -> str:
        mentor_prompts = {
            'startup_strategist': (
                "You are a Startup Strategist for VyaparAI. Help with market analysis, business planning, validation, and startup execution. "
                "Give practical, step-by-step advice, mention assumptions, and prefer lean startup approaches."
            ),
            'financial_advisor': (
                "You are a Financial Advisor for VyaparAI. Help with investment analysis, ROI, profit planning, cash flow, break-even, and runway. "
                "Show calculations when possible and state assumptions clearly."
            ),
            'marketing_guru': (
                "You are a Marketing Guru for VyaparAI. Help with customer acquisition, growth loops, positioning, pricing, and local marketing. "
                "Focus on actionable tactics and measurable KPIs."
            ),
            'tech_architect': (
                "You are a Tech Architect for VyaparAI. Help with technology choices, system design, product architecture, MVP scoping, and implementation tradeoffs. "
                "Prefer simple, scalable solutions."
            ),
            'general': (
                "You are a helpful AI business assistant for VyaparAI. Help users discover business ideas, plan execution, estimate investment, and grow responsibly. "
                "Be practical, structured, and concise."
            ),
        }

        parts = [
            mentor_prompts.get(mentor_type, mentor_prompts['general']),
            PromptTemplates.language_note(language),
            "If the user asks for a roadmap, provide phase-based guidance with milestones, risks, and metrics.",
            "If information is uncertain, say so instead of guessing. Avoid legal or financial guarantees.",
        ]

        if context:
            parts.append(f"Context: {context}")

        return "\n".join(parts)

    @staticmethod
    def roadmap_prompt(business_idea: str, user_skills: list[str], investment: float, language: str) -> str:
        return (
            f"Create a JSON roadmap for: {business_idea}\n"
            f"User skills: {', '.join(user_skills) if user_skills else 'Not provided'}\n"
            f"Investment budget: ₹{investment}\n"
            f"{PromptTemplates.language_note(language)}\n\n"
            "Return strict JSON with this schema:\n"
            "{\n"
            '  "phases": [{"title": "", "duration": "", "tasks": [""], "key_milestones": [""]}],\n'
            '  "total_duration": "",\n'
            '  "risk_mitigation": [{"risk": "", "mitigation": ""}],\n'
            '  "success_metrics": [""]\n'
            "}\n"
            "Keep the advice practical, budget-aware, and startup-friendly."
        )

    @staticmethod
    def recommendation_prompt(recommendation_type: str, budget: str | None, skills: list[str], interests: list[str], language: str) -> str:
        return (
            f"Generate startup recommendations of type '{recommendation_type}'.\n"
            f"Budget: {budget or 'Not provided'}\n"
            f"Skills: {', '.join(skills) if skills else 'Not provided'}\n"
            f"Interests: {', '.join(interests) if interests else 'Not provided'}\n"
            f"{PromptTemplates.language_note(language)}\n\n"
            "Return strict JSON with keys: recommendations, insights, next_steps.\n"
            "Each recommendation should include title, category, estimated_investment, expected_profit, difficulty, and reason."
        )

    @staticmethod
    def calculator_prompt(investment: float, monthly_expenses: float, expected_profit_percentage: float, months: int, language: str) -> str:
        return (
            f"Analyze startup ROI for investment ₹{investment}, monthly expenses ₹{monthly_expenses}, expected profit percentage {expected_profit_percentage}%, and timeline {months} months.\n"
            f"{PromptTemplates.language_note(language)}\n\n"
            "Return strict JSON with keys: monthly_profit, total_profit, total_expenses, net_profit, roi_percentage, break_even_months, suggestions.\n"
            "Show the math clearly and keep suggestions actionable."
        )
