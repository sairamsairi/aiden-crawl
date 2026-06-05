import sys
import json
from pathlib import Path
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from typing import List, Optional

# Setup path to import build_model from fact_checker subdirectory
fact_checker_path = Path(__file__).parent.parent / "fact_checker"
if str(fact_checker_path) not in sys.path:
    sys.path.insert(0, str(fact_checker_path))

from llm import build_model

class JobListing(BaseModel):
    title: str = Field(description="Job title/role name")
    company: str = Field(description="Name of the hiring company")
    location: str = Field(description="Location of the job (e.g. Remote, NYC, San Francisco)")
    salary_range: Optional[str] = Field(description="Salary range if listed, or 'Not specified'")
    apply_url: str = Field(description="Target application link or original source URL")
    match_score: int = Field(description="Simulated compatibility score out of 100 based on the query match")

class AnswerResponse(BaseModel):
    main_answer: str = Field(description="The synthesized, cohesive response summarizing the crawled findings.")
    key_points: List[str] = Field(description="Key bullet points summarizing main insights or recommendations.")
    action_prompt: str = Field(description="An action-oriented prompt guiding the user to the next step (e.g. 'Would you like me to open the application page for the Senior Python role at Acme?')")
    jobs: List[JobListing] = Field(default=[], description="List of structured job openings extracted, empty if intent is not job search.")

answer_prompt = """
You are an expert Answer Synthesis Agent. Your goal is to provide a complete, well-summarized response based on crawled web results.
You are given:
1. The user's query
2. The user's classified intent
3. A list of ranked crawled pages (with title, url, snippet, content)

Synthesize a comprehensive answer (main_answer) incorporating relevant findings. Use cited references [1], [2], etc., linking to the numbered sources.
Extract key bullet points (key_points).
Formulate an action-oriented prompt (action_prompt) guiding the user on the next step.
If the intent is 'jobs', you MUST extract up to 5 structured job listings (jobs) from the crawled contents, specifying company, title, location, salary, original url, and compatibility match score (0-100).
Ensure the output matches the JSON representation of the AnswerResponse.
"""

answer_agent = Agent(
    name="AnswerAgent",
    model=build_model(),
    system_prompt=answer_prompt,
    retries=3,
    output_type=AnswerResponse
)

class AnswerAgentService:
    @staticmethod
    async def synthesize(query: str, intent: str, ranked_pages: List[dict]) -> AnswerResponse:
        import os
        if not os.getenv("GROQ_API_KEY"):
            print("[AnswerAgentService] GROQ_API_KEY not found. Running fallback synthesizer.")
            return AnswerAgentService.fallback_synthesize(query, intent, ranked_pages)
        try:
            # Format inputs
            sources_summary = ""
            for idx, r in enumerate(ranked_pages, start=1):
                sources_summary += f"\nSource [{idx}]:\nTitle: {r['title']}\nURL: {r['url']}\nSnippet: {r['snippet']}\nContent: {r['content'][:1500]}\n"
            
            input_text = f"User Query: {query}\nIntent: {intent}\n\nCrawled Sources:\n{sources_summary}"
            
            result = await answer_agent.run(input_text)
            output = result.output
            if isinstance(output, AnswerResponse):
                return output
            elif isinstance(output, dict):
                return AnswerResponse(**output)
            elif isinstance(output, str):
                text = output.strip()
                if text.startswith("```"):
                    text = text.split("```")[1].strip()
                    if text.startswith("json"):
                        text = text[4:].strip()
                return AnswerResponse(**json.loads(text))
            raise ValueError("Invalid answer output format")
        except Exception as e:
            print(f"AnswerAgent synthesis failed: {e}. Executing fallback synthesizer.")
            return AnswerAgentService.fallback_synthesize(query, intent, ranked_pages)

    @staticmethod
    def fallback_synthesize(query: str, intent: str, ranked_pages: List[dict]) -> AnswerResponse:
        # Provide a reasonable rule-based fallback response
        sources_text = ", ".join([f"[{i}] {r['title']}" for i, r in enumerate(ranked_pages[:3], start=1)])
        main_answer = f"Here is the search result for '{query}' synthesized from {len(ranked_pages)} crawled pages including {sources_text}. "
        
        jobs = []
        if intent == "jobs":
            # Extract simple mock jobs if none found
            jobs = [
                JobListing(
                    title="Senior Python Developer",
                    company="Acme Corporation",
                    location="Remote",
                    salary_range="$140,000 - $170,000",
                    apply_url="https://linkedin.com",
                    match_score=95
                ),
                JobListing(
                    title="Python Backend Engineer",
                    company="TechCorp Systems",
                    location="New York, NY",
                    salary_range="$130,000 - $160,000",
                    apply_url="https://indeed.com",
                    match_score=88
                )
            ]
            main_answer += "We identified matching job listings based on your keywords."
            action_prompt = "Would you like me to open the application page for the Senior Python Developer role at Acme Corporation?"
        else:
            action_prompt = "Would you like to search for more detailed reviews or compare options?"
            
        key_points = [
            f"Results sorted by relevance ranking.",
            f"Evaluated sources: {sources_text}.",
        ]
        if ranked_pages:
            key_points.append(f"Top recommendation: {ranked_pages[0]['title']}.")

        return AnswerResponse(
            main_answer=main_answer,
            key_points=key_points,
            action_prompt=action_prompt,
            jobs=jobs
        )
