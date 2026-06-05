import sys
import json
from pathlib import Path
from pydantic import BaseModel
from pydantic_ai import Agent
from enum import Enum
from typing import List

# Setup path to import build_model from fact_checker subdirectory
fact_checker_path = Path(__file__).parent.parent / "fact_checker"
if str(fact_checker_path) not in sys.path:
    sys.path.insert(0, str(fact_checker_path))

from llm import build_model

class UserIntent(str, Enum):
    JOB_SEARCH = "jobs"
    PRODUCT_RESEARCH = "products"
    EVENT_FINDER = "events"
    SERVICE_LOCATOR = "services"
    GENERAL_QNA = "general"

class IntentResult(BaseModel):
    intent: UserIntent
    confidence: float
    keywords: List[str]
    suggested_queries: List[str]

intent_prompt = """
You are an AI query intent classifier. Analyze the user's query and classify it into one of these intents:
1. 'jobs' (for finding job openings, vacancies, careers, internship options, hiring posts, remote jobs)
2. 'products' (for shopping, product reviews, mechanical keyboards, software comparisons, specs, best buys)
3. 'events' (for conferences, meetups, bookings, festivals, workshops, live concerts)
4. 'services' (for local service providers, dental clinics, barbershops, plumbers, cloud hostings, developers)
5. 'general' (for general facts, questions, how-tos, descriptions, news, and everything else)

Extract the main keywords and generate 2-3 specific search queries that can be used on a search engine like DuckDuckGo to find information.
Ensure you return only the structured JSON representation of the IntentResult type.
"""

intent_classifier_agent = Agent(
    name="IntentClassifierAgent",
    model=build_model(),
    system_prompt=intent_prompt,
    retries=3,
    output_type=IntentResult
)

class IntentClassifier:
    @staticmethod
    async def classify(query: str) -> IntentResult:
        import os
        if not os.getenv("GROQ_API_KEY"):
            print("[IntentClassifier] GROQ_API_KEY not found. Running fallback rule-based classifier.")
            return IntentClassifier.fallback_classify(query)
        try:
            result = await intent_classifier_agent.run(query)
            output = result.output
            if isinstance(output, IntentResult):
                return output
            elif isinstance(output, dict):
                return IntentResult(**output)
            elif isinstance(output, str):
                # Attempt to parse json
                text = output.strip()
                if text.startswith("```"):
                    text = text.split("```")[1].strip()
                    if text.startswith("json"):
                        text = text[4:].strip()
                return IntentResult(**json.loads(text))
            raise ValueError("Invalid output format")
        except Exception as e:
            print(f"Agent classification failed: {e}. Running fallback rule-based classifier.")
            return IntentClassifier.fallback_classify(query)

    @staticmethod
    def fallback_classify(query: str) -> IntentResult:
        query_lower = query.lower()
        intent = UserIntent.GENERAL_QNA
        words = query.split()
        keywords = [word.strip("?,.!") for word in words if len(word) > 3]
        
        # Rule indicators
        job_keywords = ["job", "career", "hiring", "opening", "vacancy", "internship", "developer", "engineer", "designer", "remote work"]
        product_keywords = ["best", "buy", "review", "keyboard", "mouse", "phone", "price", "purchase", "shopping", "laptop", "pc"]
        event_keywords = ["event", "conference", "meetup", "concert", "festival", "booking", "pycon", "nyc", "hackathon"]
        service_keywords = ["service", "plumber", "barber", "dentist", "clinic", "hosting", "developer agency", "cleaner"]

        if any(k in query_lower for k in job_keywords):
            intent = UserIntent.JOB_SEARCH
        elif any(k in query_lower for k in product_keywords):
            intent = UserIntent.PRODUCT_RESEARCH
        elif any(k in query_lower for k in event_keywords):
            intent = UserIntent.EVENT_FINDER
        elif any(k in query_lower for k in service_keywords):
            intent = UserIntent.SERVICE_LOCATOR
            
        return IntentResult(
            intent=intent,
            confidence=0.75,
            keywords=keywords[:5],
            suggested_queries=[query]
        )
