import asyncio
from datetime import datetime
from typing import List, Dict, Any
from duckduckgo_search import DDGS

from services.intent_classifier import IntentClassifier, IntentResult
from services.web_crawler import WebCrawler, CrawledContent
from services.ranking_service import SearchRanker, RankedResult
from fact_checker.answer_agent import AnswerAgentService, AnswerResponse

class SearchAgentService:
    @staticmethod
    async def run_pipeline(query: str) -> Dict[str, Any]:
        """Runs the complete end-to-end crawling and answering pipeline for a user query."""
        # Step 1: Classify user intent
        print(f"[Pipeline] Classifying intent for query: '{query}'")
        intent_result: IntentResult = await IntentClassifier.classify(query)
        print(f"[Pipeline] Intent: {intent_result.intent} (Confidence: {intent_result.confidence})")
        
        # Step 2: Search web using DuckDuckGo
        search_queries = intent_result.suggested_queries
        if not search_queries:
            search_queries = [query]
            
        search_results = []
        # Run DuckDuckGo text searches sequentially in a thread pool
        for s_query in search_queries[:2]:  # Limit to top 2 suggested queries
            print(f"[Pipeline] Searching DuckDuckGo for: '{s_query}'")
            try:
                loop = asyncio.get_running_loop()
                def run_ddg():
                    with DDGS() as ddgs:
                        # Convert generator to list immediately
                        return list(ddgs.text(s_query, max_results=5))
                
                results = await loop.run_in_executor(None, run_ddg)
                if results:
                    search_results.extend(results)
            except Exception as e:
                print(f"[Pipeline] Search error for query '{s_query}': {e}")
                
        # Deduplicate results by URL
        seen_urls = set()
        unique_search_results = []
        for r in search_results:
            url = r.get("href")
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_search_results.append(r)
                
        # Crawl top 4 results to maintain speedy responses
        target_results = unique_search_results[:4]
        
        if not target_results:
            print("[Pipeline] No search results returned.")
            fallback_pages = [
                CrawledContent(
                    url="https://google.com",
                    title="Web Search",
                    content="No detailed online results found.",
                    links=[],
                    fetch_time=datetime.utcnow(),
                    status_code=404
                )
            ]
            ranked = SearchRanker.rank_results(fallback_pages, query, intent_result.keywords)
            answer = AnswerAgentService.fallback_synthesize(query, intent_result.intent, [r.model_dump() for r in ranked])
            return {
                "intent": intent_result.intent,
                "confidence_score": f"{int(intent_result.confidence * 100)}%",
                "confidence_level": "medium",
                "summary": answer.main_answer,
                "recommendation": answer.action_prompt,
                "key_claim": query,
                "key_claim_verdict": "UNVERIFIABLE",
                "key_claim_reason": "No search results returned.",
                "note": "SearchShield AI Universal Assistant",
                "synthesized_answer": answer.main_answer,
                "key_points": answer.key_points,
                "action_prompt": answer.action_prompt,
                "jobs": [j.model_dump() for j in answer.jobs],
                "sources": [s.model_dump() for s in ranked]
            }
            
        # Step 3: Crawl the target pages concurrently
        crawler = WebCrawler()
        urls_to_crawl = [r["href"] for r in target_results]
        print(f"[Pipeline] Crawling {len(urls_to_crawl)} URLs...")
        crawled_pages = await crawler.crawl_multiple(urls_to_crawl)
        
        # Sync titles/snippets into crawled content if titles are empty
        for crawled in crawled_pages:
            for sr in target_results:
                if sr["href"] == crawled.url:
                    if not crawled.title:
                        crawled.title = sr.get("title", "")
                    break
                    
        # Step 4: Rank results using TF-IDF and domain reputation
        print("[Pipeline] Ranking crawled contents...")
        ranked_results: List[RankedResult] = SearchRanker.rank_results(
            crawled_pages, query, intent_result.keywords
        )
        
        # Step 5: Synthesize final answer & actions
        print("[Pipeline] Synthesizing final answer...")
        ranked_pages_dump = [r.model_dump() for r in ranked_results]
        for r_dump in ranked_pages_dump:
            for cp in crawled_pages:
                if cp.url == r_dump["url"]:
                    r_dump["content"] = cp.content
                    break
                    
        answer_result: AnswerResponse = await AnswerAgentService.synthesize(
            query, intent_result.intent, ranked_pages_dump
        )
        
        confidence_level = "high" if intent_result.confidence >= 0.85 else "medium" if intent_result.confidence >= 0.6 else "low"
        
        # Construct backward-compatible response dictionary
        return {
            "intent": intent_result.intent,
            "confidence_score": f"{int(intent_result.confidence * 100)}%",
            "confidence_level": confidence_level,
            "summary": answer_result.main_answer,
            "recommendation": answer_result.action_prompt,
            "key_claim": query,
            "key_claim_verdict": intent_result.intent.upper(),
            "key_claim_reason": f"Analyzed query with intent: {intent_result.intent}",
            "note": "SearchShield AI Intelligent Search Assistant",
            "synthesized_answer": answer_result.main_answer,
            "key_points": answer_result.key_points,
            "action_prompt": answer_result.action_prompt,
            "jobs": [j.model_dump() for j in answer_result.jobs],
            "sources": [s.model_dump() for s in ranked_results]
        }
