# Implementation Plan: Converting TruthShield to Intelligent Web Crawler

## Quick Start: What to Build

### Current Problem

- **TruthShield** = Fact-checking specialist (validates existing claims)
- **Problem Statement 5** = Answer Agent (finds info & enables actions)

### Solution

Add 5 new modules to transform TruthShield into a full-featured answer agent.

---

## 🏗️ Module 1: Web Crawler

### File: `backend/crawler/web_crawler.py`

```python
# Key Classes:
class WebCrawler:
    """Fetches and parses web content"""
    - async crawl(url: str) -> CrawledContent
    - async crawl_multiple(urls: list[str]) -> list[CrawledContent]
    - extract_text(html: str) -> str
    - extract_links(html: str, base_url: str) -> list[str]
    - respectful_crawl(url: str, rate_limit: float = 1.0)

class CrawledContent(BaseModel):
    url: str
    title: str
    content: str
    links: list[str]
    fetch_time: datetime
    status_code: int
```

### Dependencies

```
beautifulsoup4>=4.12.0
selenium>=4.15.0
lxml>=4.9.0
httpx>=0.25.0
```

### Usage Example

```python
crawler = WebCrawler()
content = await crawler.crawl("https://example.com")
print(content.title)  # Page title
print(content.content)  # Clean text
```

---

## 🎯 Module 2: Intent Classifier

### File: `backend/agents/intent_classifier.py`

```python
# Enums:
class UserIntent(Enum):
    GENERAL_QUESTION = "general"      # What is X?
    JOB_SEARCH = "jobs"               # Find jobs
    PRODUCT_RESEARCH = "products"     # Best product reviews
    EVENT_FINDER = "events"           # Find events
    SERVICE_LOCATOR = "services"      # Find services
    COMPARISON = "comparison"         # Compare X vs Y
    CURRENT_EVENTS = "news"           # Latest news

# Agent:
class IntentClassifierAgent:
    async def classify(query: str) -> IntentResult
    async def extract_keywords(query: str) -> list[str]
    async def get_search_filters(intent: UserIntent) -> dict

class IntentResult(BaseModel):
    intent: UserIntent
    confidence: float  # 0-1
    keywords: list[str]
    suggested_sources: list[str]
```

### Usage Example

```python
classifier = IntentClassifierAgent()
result = await classifier.classify("Find me remote Python jobs in NYC")
# Result:
# - intent: UserIntent.JOB_SEARCH
# - confidence: 0.95
# - keywords: ["Python", "remote", "NYC"]
# - suggested_sources: ["linkedin.com", "indeed.com", "builtin.com"]
```

---

## 📊 Module 3: Ranking Engine

### File: `backend/ranking/search_ranker.py`

```python
class SearchRanker:
    """Ranks search results by relevance"""

    def rank_results(
        results: list[SearchResult],
        query: str,
        intent: UserIntent
    ) -> list[RankedResult]:
        # Scoring factors:
        # 1. TF-IDF relevance to query
        # 2. Domain authority (from database)
        # 3. Content freshness
        # 4. User engagement (clicks, time)
        # 5. Intent-specific signals

    def calculate_tfidf_score(text: str, query: str) -> float
    def get_domain_authority(domain: str) -> float  # 0-100
    def calculate_freshness_score(published_date: datetime) -> float

class RankedResult(BaseModel):
    url: str
    title: str
    snippet: str
    domain: str
    relevance_score: float  # 0-100
    authority_score: float  # 0-100
    freshness_score: float  # 0-100
    combined_score: float   # weighted combination
    rank: int
```

### Usage Example

```python
ranker = SearchRanker()
ranked = ranker.rank_results(search_results, "best python framework", UserIntent.GENERAL_QUESTION)
# Returns top 5 most relevant results sorted by combined_score
```

---

## 💼 Module 4: Job Pipeline

### File: `backend/integrations/job_pipeline.py`

```python
class JobExtractor:
    """Extracts structured job data from listings"""

    async def parse_job_listing(html: str) -> JobListing
    async def search_jobs(query: str, filters: dict) -> list[JobListing]
    async def match_user_skills(job: JobListing, skills: list[str]) -> MatchScore

class JobListing(BaseModel):
    title: str
    company: str
    location: str
    salary_range: Optional[str]
    job_type: str  # "Full-time", "Remote", "Contract"
    description: str
    requirements: list[str]
    posted_date: datetime
    application_url: str
    source: str  # "linkedin", "indeed", "builtin"
    match_score: float  # 0-100 based on user skills

class JobRecommender:
    """Recommends jobs and generates application prompts"""

    async def recommend_jobs(
        keywords: str,
        user_profile: UserProfile,
        limit: int = 5
    ) -> list[JobListing]:
        # Ranks jobs by match_score

    async def generate_apply_prompt(job: JobListing, user: User) -> str:
        # Returns: "Found Senior Python Developer at Acme. Would you like to apply?"
```

### Usage Example

```python
job_pipeline = JobPipeline()
jobs = await job_pipeline.search_jobs(
    "Python developer",
    filters={"location": "remote", "salary_min": 100000}
)
# Returns ranked list of 5 best matching jobs with application links
```

---

## 💡 Module 5: Answer Agent

### File: `backend/agents/answer_agent.py`

```python
class AnswerAgent:
    """Synthesizes answers from multiple sources"""

    async def answer_query(
        query: str,
        search_results: list[RankedResult],
        crawled_content: list[CrawledContent]
    ) -> Answer:
        # Process: Extract facts → Synthesize → Rank sources → Format answer

class Answer(BaseModel):
    main_answer: str
    key_points: list[str]
    sources: list[Citation]
    confidence_score: float  # 0-100
    requires_action: bool
    suggested_action: Optional[str]

class Citation(BaseModel):
    url: str
    title: str
    domain: str
    snippet: str
    relevance: float

class ActionHandler:
    """Handles actionable intents"""

    async def get_action_prompt(
        intent: UserIntent,
        results: list[RankedResult]
    ) -> ActionPrompt:
        # Returns: "Would you like to apply for this job?"

class ActionPrompt(BaseModel):
    text: str  # The prompt to show user
    action_type: str  # "apply_job", "visit_link", "book_event"
    action_data: dict  # Context for the action
```

### Usage Example

```python
answer_agent = AnswerAgent()
answer = await answer_agent.answer_query(
    query="Find me remote Python developer jobs",
    search_results=ranked_results,
    crawled_content=crawled_pages
)
# Returns structured answer with job listings and action prompts
```

---

## 🔄 New API Endpoints

### File: `backend/routers/crawler_routes.py`

```python
@router.post("/query")
async def query(
    body: QueryRequest,
    user = Depends(get_current_user)
) -> QueryResponse:
    """Main endpoint: user asks question, get intelligent answer"""
    # 1. Classify intent
    # 2. Search web
    # 3. Crawl top results
    # 4. Rank by relevance
    # 5. Generate answer
    # 6. Detect actions
    # 7. Return formatted result

@router.post("/search")
async def search(
    body: SearchRequest,
    user = Depends(get_current_user)
) -> SearchResponse:
    """Search and rank results without crawling"""

@router.get("/jobs/search")
async def search_jobs(
    keywords: str,
    location: Optional[str] = None,
    salary_min: Optional[int] = None
) -> list[JobListing]:
    """Dedicated job search endpoint"""

@router.post("/apply")
async def apply_job(
    body: JobApplicationRequest,
    user = Depends(get_current_user)
) -> ApplicationResponse:
    """Helper to apply to jobs"""
```

---

## 📊 Database Schema Updates

### New Tables: `backend/models.py`

```python
class SearchResult(Base):
    __tablename__ = "search_results"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    query = Column(String)
    results = Column(JSON)  # Cached results
    created_at = Column(DateTime, default=datetime.utcnow)

class JobApplication(Base):
    __tablename__ = "job_applications"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    job_url = Column(String)
    job_title = Column(String)
    company = Column(String)
    applied_date = Column(DateTime)
    status = Column(String)  # "draft", "submitted", "rejected"

class DomainAuthority(Base):
    __tablename__ = "domain_authority"
    id = Column(Integer, primary_key=True)
    domain = Column(String, unique=True)
    authority_score = Column(Float)  # 0-100
    updated_at = Column(DateTime)
```

---

## 🎨 Frontend Updates

### New Components: `frontend/src/components/`

```javascript
// QueryInput.js - Replace textarea with smart query input
// IntentDisplay.js - Show detected intent with confidence
// ResultCard.js - Display individual results with rank
// ActionButton.js - "Apply", "Visit", "Book Event" buttons
// JobResults.js - Specialized job results view
// Citation.js - Formatted citations with sources
```

### Updated Dashboard

```javascript
// Old: Paste text → Get verdict
// New: Enter question → Get ranked answer with actions
```

---

## 📈 Implementation Schedule

### Week 1: Foundation

- [ ] Build WebCrawler module with BeautifulSoup
- [ ] Create IntentClassifier agent
- [ ] Setup new database tables
- [ ] Write unit tests

### Week 2: Ranking & Job Pipeline

- [ ] Implement SearchRanker with TF-IDF
- [ ] Build JobExtractor
- [ ] Create JobRecommender
- [ ] Test job search end-to-end

### Week 3: Answer Agent & Integration

- [ ] Build AnswerAgent
- [ ] Implement ActionHandler
- [ ] Create new API endpoints
- [ ] Add error handling & fallbacks

### Week 4: Frontend & Polish

- [ ] Build new React components
- [ ] Update Dashboard UI
- [ ] Test full pipeline end-to-end
- [ ] Performance optimization

---

## 🧪 Testing Strategy

### Unit Tests

```python
# test_web_crawler.py
test_crawl_valid_url()
test_crawl_invalid_url()
test_extract_text()

# test_intent_classifier.py
test_classify_job_query()
test_classify_product_query()
test_extract_keywords()

# test_search_ranker.py
test_tfidf_scoring()
test_domain_authority()
test_rank_results()
```

### Integration Tests

```python
# test_end_to_end.py
test_full_query_pipeline()
test_job_search_workflow()
test_action_detection()
```

### Performance Tests

```python
# test_performance.py
test_crawler_speed()
test_ranking_speed()
test_answer_generation_speed()
```

---

## 🚀 Deployment Considerations

### Docker Updates: `backend/Dockerfile`

```dockerfile
# Add new dependencies
RUN pip install beautifulsoup4 scrapy scikit-learn

# Increase timeout for crawler operations
ENV CRAWLER_TIMEOUT=30
```

### Environment Variables: `.env`

```env
# Crawling
CRAWLER_RATE_LIMIT=1.0
CRAWLER_TIMEOUT=30

# Job APIs
LINKEDIN_API_KEY=...
INDEED_API_KEY=...

# Ranking
DOMAIN_AUTHORITY_CACHE_TTL=3600
```

---

## 📚 Key Algorithms to Implement

### TF-IDF Ranking

```
Score = (Term Frequency × log(Total Docs / Docs with term))
```

### Combined Ranking

```
Final Score =
  (0.4 × TF-IDF Score) +
  (0.3 × Domain Authority) +
  (0.2 × Freshness Score) +
  (0.1 × Engagement Score)
```

### Job Matching

```
Match Score =
  (Skill Match %) ×
  (Location Match %) ×
  (Salary Match %)
```

---

## ✅ Success Criteria

After implementation, TruthShield should:

- [x] Handle general queries: "What's X?" → Ranked answers with sources
- [x] Detect job queries: "Find me jobs" → Job listings with apply button
- [x] Detect product queries: "Best X?" → Ranked product reviews
- [x] Support 5+ intent types
- [x] Return answers in <5 seconds
- [x] Provide action prompts for 80%+ of relevant queries
- [x] Show proper citations for all sources
- [x] Achieve 85%+ accuracy in intent classification

---

## 📝 Code Quality Standards

- Type hints on all functions
- Docstrings for all classes/methods
- Unit test coverage >80%
- Error handling with fallbacks
- Logging at INFO and ERROR levels
- Async-first implementation

---

## 🎯 Priority Order

**MUST HAVE (MVP)**

1. WebCrawler + ranking engine
2. IntentClassifier
3. AnswerAgent
4. Query endpoint

**SHOULD HAVE** 5. Job pipeline 6. UI improvements

**NICE TO HAVE** 7. Product search 8. Event finder 9. Caching optimization
