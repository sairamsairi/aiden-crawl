# Implementation Checklist: From TruthShield to SearchShield

## 📋 Master Checklist - Complete Implementation

---

## PHASE 1: Planning & Setup (Week 0)

- [ ] **Review Documentation**
  - [ ] Read QUICK_REFERENCE.md (5 min)
  - [ ] Read VISUAL_COMPARISON.md (15 min)
  - [ ] Review IMPLEMENTATION_PLAN.md (30 min)
  - [ ] Discuss PROJECT_STRUCTURE.md with team (20 min)

- [ ] **Environment Setup**
  - [ ] Create new branch: `git checkout -b feature/searchshield`
  - [ ] Update requirements.txt with new dependencies:
    - [ ] beautifulsoup4
    - [ ] scrapy
    - [ ] scikit-learn
    - [ ] lxml
    - [ ] httpx
  - [ ] Run `pip install -r requirements.txt`
  - [ ] Test that imports work

- [ ] **Database Preparation**
  - [ ] Add new models to models.py:
    - [ ] SearchResult
    - [ ] JobApplication
    - [ ] DomainAuthority
  - [ ] Create database migration
  - [ ] Test database connections

- [ ] **Project Structure**
  - [ ] Create `backend/crawler/` directory
  - [ ] Create `backend/ranking/` directory
  - [ ] Create `backend/integrations/` directory
  - [ ] Create `backend/agents/intent_classifier.py`
  - [ ] Add `__init__.py` files to all directories

---

## PHASE 2: Web Crawler Module (Week 1 - Days 1-2)

### ✅ Subtask: Basic Web Crawler

- [ ] **Create `backend/crawler/web_crawler.py`**
  - [ ] Define CrawledContent model (5 fields: url, title, content, links, status_code)
  - [ ] Implement WebCrawler class
  - [ ] Add method: `async crawl(url: str) -> CrawledContent`
  - [ ] Add method: `extract_text(html: str) -> str` (using BeautifulSoup)
  - [ ] Add method: `extract_links(html: str, base_url: str) -> list[str]`
  - [ ] Add rate limiting decorator (1 request/second)
  - [ ] Add robots.txt checking
  - [ ] Add error handling for invalid URLs
  - [ ] Add timeout handling (30 seconds)

- [ ] **Create `backend/crawler/parser.py`**
  - [ ] Implement content parser
  - [ ] Add method: `parse_html(html: str) -> dict` (title, body, metadata)
  - [ ] Add method: `clean_text(text: str) -> str`
  - [ ] Handle edge cases (empty content, encoding issues)

- [ ] **Unit Tests for Crawler**
  - [ ] test_crawl_valid_url() - Should return CrawledContent
  - [ ] test_crawl_invalid_url() - Should handle gracefully
  - [ ] test_extract_text() - Should extract readable text
  - [ ] test_extract_links() - Should find all links
  - [ ] test_rate_limiting() - Should respect delays
  - [ ] test_robots_txt() - Should check robots.txt
  - [ ] Mock external HTTP requests

- [ ] **Documentation**
  - [ ] Add docstrings to all methods
  - [ ] Write README for crawler module
  - [ ] Document usage examples

---

## PHASE 2: Intent Classifier Module (Week 1 - Days 3-4)

### ✅ Subtask: Intent Classification

- [ ] **Create `backend/agents/intent_classifier.py`**
  - [ ] Define UserIntent enum:
    - [ ] GENERAL_QUESTION
    - [ ] JOB_SEARCH
    - [ ] PRODUCT_RESEARCH
    - [ ] EVENT_FINDER
    - [ ] SERVICE_LOCATOR
    - [ ] COMPARISON
  - [ ] Define IntentResult model
  - [ ] Create IntentClassifierAgent (using Pydantic-AI)
  - [ ] Add method: `async classify(query: str) -> IntentResult`
  - [ ] Add method: `async extract_keywords(query: str) -> list[str]`
  - [ ] Add method: `get_suggested_sources(intent: UserIntent) -> list[str]`
  - [ ] Add confidence scoring (0-1)
  - [ ] Add fallback to GENERAL_QUESTION if uncertain

- [ ] **System Prompt Engineering**
  - [ ] Write clear system prompt for intent classification
  - [ ] Include examples for each intent type
  - [ ] Test with 20+ sample queries
  - [ ] Refine based on test results

- [ ] **Unit Tests for Intent Classifier**
  - [ ] test_classify_job_query() - Should detect JOB_SEARCH
  - [ ] test_classify_product_query() - Should detect PRODUCT_RESEARCH
  - [ ] test_classify_general_query() - Should detect GENERAL_QUESTION
  - [ ] test_classify_comparison() - Should detect COMPARISON
  - [ ] test_confidence_scoring() - Should return 0-1 confidence
  - [ ] test_keyword_extraction() - Should find relevant keywords
  - [ ] test_suggested_sources() - Should return appropriate sources

- [ ] **Manual Testing**
  - [ ] Test 30+ real-world queries
  - [ ] Document accuracy on test set
  - [ ] Refine agent prompt if needed

- [ ] **Documentation**
  - [ ] Add docstrings
  - [ ] Write README with examples
  - [ ] Document enum values

---

## PHASE 2: Search Ranking Module (Week 1 - Days 5)

### ✅ Subtask: Result Ranking

- [ ] **Create `backend/ranking/search_ranker.py`**
  - [ ] Define RankedResult model (url, title, snippet, relevance_score, rank, etc.)
  - [ ] Implement SearchRanker class
  - [ ] Add method: `rank_results(results, query, intent) -> list[RankedResult]`

- [ ] **Create `backend/ranking/scorer.py`**
  - [ ] Implement TF-IDF scoring:
    - [ ] `calculate_tfidf_score(text: str, query: str) -> float`
    - [ ] `build_tfidf_vectorizer(texts: list[str])`
  - [ ] Implement domain authority scoring:
    - [ ] `get_domain_authority(domain: str) -> float` (from cache)
    - [ ] Handle unknown domains (default to 50)
  - [ ] Implement freshness scoring:
    - [ ] `calculate_freshness_score(published_date: datetime) -> float`
  - [ ] Implement combined scoring:
    - [ ] `combine_scores(tfidf, authority, freshness) -> float`
    - [ ] Weights: 40% relevance, 30% authority, 20% freshness, 10% engagement

- [ ] **Create Domain Authority Database**
  - [ ] Populate common domains (techcrunch.com=95, stackoverflow.com=90, etc.)
  - [ ] Implement caching (TTL: 1 hour)
  - [ ] Add manual update capability

- [ ] **Unit Tests for Ranker**
  - [ ] test_tfidf_scoring() - Check calculation
  - [ ] test_domain_authority() - Verify scores
  - [ ] test_freshness_calculation() - Check date scoring
  - [ ] test_combined_score() - Verify weighting
  - [ ] test_rank_order() - Verify sorting

- [ ] **Benchmarking**
  - [ ] Run on 50 test queries
  - [ ] Compare to baseline (DuckDuckGo order)
  - [ ] Manual quality check

---

## PHASE 3: Job Pipeline Module (Week 2 - Days 1-3)

### ✅ Subtask: Job Search & Extraction

- [ ] **Create `backend/integrations/job_extractor.py`**
  - [ ] Define JobListing model:
    - [ ] title, company, location, salary_range
    - [ ] job_type, description, requirements
    - [ ] posted_date, application_url, source
    - [ ] match_score
  - [ ] Create JobExtractor class
  - [ ] Add method: `async parse_job_listing(html: str) -> JobListing`
  - [ ] Add parsers for common formats (LinkedIn, Indeed, BuiltIn)
  - [ ] Extract structured data from HTML

- [ ] **Create `backend/integrations/job_pipeline.py`**
  - [ ] Implement JobRecommender class
  - [ ] Add method: `async search_jobs(keywords, filters) -> list[JobListing]`
  - [ ] Add method: `async match_user_skills(job, skills) -> float` (0-100)
  - [ ] Add job matching algorithm:
    - [ ] Parse required skills from job description
    - [ ] Compare to user skills
    - [ ] Calculate match percentage
  - [ ] Add filtering:
    - [ ] By location (remote/on-site/hybrid)
    - [ ] By salary range
    - [ ] By job type (full-time/contract/part-time)
  - [ ] Add sorting by match score

- [ ] **Job Scraping Setup**
  - [ ] For MVP, can use public job APIs or manual scraping
  - [ ] Options:
    - [ ] LinkedIn job search (public URLs)
    - [ ] Indeed API or scraping
    - [ ] BuiltIn.com job listings
  - [ ] Respect robots.txt for each site

- [ ] **Unit Tests for Job Pipeline**
  - [ ] test_parse_job_listing() - Should extract fields
  - [ ] test_search_jobs() - Should return jobs
  - [ ] test_skill_matching() - Should calculate score
  - [ ] test_filter_by_location() - Should filter correctly
  - [ ] test_sort_by_match() - Should rank top matches

- [ ] **Documentation**
  - [ ] Document JobListing schema
  - [ ] Add usage examples

---

## PHASE 3: Answer Agent Module (Week 2 - Days 4-5)

### ✅ Subtask: Answer Generation

- [ ] **Create `backend/agents/answer_agent.py`**
  - [ ] Define Answer model:
    - [ ] main_answer (string)
    - [ ] key_points (list)
    - [ ] sources (list of Citation)
    - [ ] confidence_score (0-100)
    - [ ] requires_action (bool)
    - [ ] suggested_action (optional string)
  - [ ] Define Citation model:
    - [ ] url, title, domain, snippet, relevance
  - [ ] Implement AnswerAgent class (using Pydantic-AI)
  - [ ] Add method: `async answer_query(query, search_results, crawled_content) -> Answer`
  - [ ] Implement synthesis algorithm:
    - [ ] Extract key facts from sources
    - [ ] Remove duplicates
    - [ ] Synthesize into coherent answer
    - [ ] Track citations for each fact
  - [ ] Add confidence scoring based on:
    - [ ] Agreement between sources
    - [ ] Source authority
    - [ ] Recency of information

- [ ] **Create Action Handler**
  - [ ] Define ActionPrompt model:
    - [ ] text (what to show user)
    - [ ] action_type (apply_job, visit_link, book_event)
    - [ ] action_data (context)
  - [ ] Implement ActionHandler class
  - [ ] Add method: `async get_action_prompt(intent, results) -> Optional[ActionPrompt]`
  - [ ] Implement action-specific logic:
    - [ ] For jobs: "Apply for Senior Developer at X?"
    - [ ] For products: "Visit Amazon for this item?"
    - [ ] For events: "Book PyCon now?"

- [ ] **Unit Tests for Answer Agent**
  - [ ] test_answer_generation() - Should create coherent answer
  - [ ] test_citation_tracking() - Should link facts to sources
  - [ ] test_confidence_scoring() - Should score 0-100
  - [ ] test_action_detection() - Should identify actionable intent
  - [ ] test_action_prompt_generation() - Should create prompts

- [ ] **Manual Testing**
  - [ ] Test 20+ different query types
  - [ ] Verify answer quality
  - [ ] Check citation accuracy

---

## PHASE 4: API Integration (Week 3 - Days 1-2)

### ✅ Subtask: New API Routes

- [ ] **Create `backend/routers/crawler_routes.py`**
  - [ ] Add endpoint: `POST /query` - Main search endpoint
    - [ ] Input: QueryRequest (query: str)
    - [ ] Process: Intent → Search → Crawl → Rank → Answer
    - [ ] Output: QueryResponse (answer, sources, actions)
    - [ ] Add error handling
    - [ ] Add logging
    - [ ] Performance target: <5 seconds
  - [ ] Add endpoint: `GET /search` - Quick search without crawling
    - [ ] Input: SearchRequest (query: str)
    - [ ] Output: List of ranked results
  - [ ] Add endpoint: `GET /jobs/search` - Job search
    - [ ] Input: keywords, location (optional), salary_min (optional)
    - [ ] Output: List of JobListing
  - [ ] Add endpoint: `POST /apply` - Job application helper
    - [ ] Input: JobApplicationRequest
    - [ ] Output: ApplicationResponse
    - [ ] Track in database

- [ ] **Update `backend/main.py`**
  - [ ] Import new router
  - [ ] Include crawler_routes router
  - [ ] Add new endpoints to OpenAPI docs

- [ ] **Add Request/Response Models**
  - [ ] QueryRequest, QueryResponse
  - [ ] SearchRequest, SearchResponse
  - [ ] JobApplicationRequest, ApplicationResponse

- [ ] **Error Handling**
  - [ ] Add try-catch in all endpoints
  - [ ] Return meaningful error messages
  - [ ] Log errors for debugging
  - [ ] Graceful degradation

- [ ] **Unit Tests for Routes**
  - [ ] test_query_endpoint() - Should return Answer
  - [ ] test_search_endpoint() - Should return results
  - [ ] test_jobs_endpoint() - Should return jobs
  - [ ] test_apply_endpoint() - Should track application
  - [ ] test_error_handling() - Should handle errors gracefully

---

## PHASE 4: Frontend Components (Week 3 - Days 3-4)

### ✅ Subtask: React Components

- [ ] **Update `frontend/src/components/`**
  - [ ] Create QueryInput.js
    - [ ] Replace textarea with text input
    - [ ] Add suggestions/autocomplete
    - [ ] Add intent display (if detected)
  - [ ] Create ResultCard.js
    - [ ] Display individual result
    - [ ] Show rank, relevance score
    - [ ] Show domain authority
    - [ ] Add source link
  - [ ] Create Citation.js
    - [ ] Display citation information
    - [ ] Link to source
    - [ ] Show snippet
  - [ ] Create ActionButton.js
    - [ ] "Apply Now" button
    - [ ] "Visit Site" button
    - [ ] "Book Event" button
    - [ ] Handle clicks
  - [ ] Create JobResults.js
    - [ ] Specialized view for job results
    - [ ] Show match score
    - [ ] Show salary
    - [ ] Show apply button

- [ ] **Update Dashboard.js**
  - [ ] Replace text paste with query input
  - [ ] Update result display
  - [ ] Show detected intent
  - [ ] Show rankings/confidence
  - [ ] Add action buttons
  - [ ] Improve UX/styling

- [ ] **Update api.js**
  - [ ] Add `querySearch(text, token)` function
  - [ ] Add `searchJobs(keywords, filters, token)` function
  - [ ] Add `applyJob(jobId, token)` function
  - [ ] Error handling for each

- [ ] **Update App.js**
  - [ ] If needed, update routing
  - [ ] Add Search page route
  - [ ] Add Job page route

- [ ] **Styling Updates**
  - [ ] Update App.css
  - [ ] Add components CSS
  - [ ] Mobile responsive design
  - [ ] Dark/light mode support (optional)

- [ ] **Frontend Testing**
  - [ ] Test QueryInput component
  - [ ] Test ResultCard component
  - [ ] Test ActionButton clicks
  - [ ] Manual end-to-end testing

---

## PHASE 4: Database & Models (Week 3 - Day 5)

### ✅ Subtask: Database Schema

- [ ] **Update `backend/models.py`**
  - [ ] Add SearchResult model
  - [ ] Add JobApplication model
  - [ ] Add DomainAuthority model
  - [ ] Add UserSkills model (for job matching)

- [ ] **Database Migration**
  - [ ] Create tables
  - [ ] Test table creation
  - [ ] Verify schema

- [ ] **Seed Data**
  - [ ] Populate DomainAuthority table with known domains
  - [ ] Add test users if needed

---

## PHASE 5: Testing & Optimization (Week 4)

### ✅ Subtask: Comprehensive Testing

- [ ] **Unit Tests**
  - [ ] Test all crawler functions
  - [ ] Test all agent functions
  - [ ] Test all ranking functions
  - [ ] Coverage: >80%
  - [ ] Run: `pytest --cov=backend tests/`

- [ ] **Integration Tests**
  - [ ] Test full query pipeline
  - [ ] Test job search pipeline
  - [ ] Test end-to-end flow
  - [ ] Test error scenarios

- [ ] **Performance Testing**
  - [ ] Benchmark crawler speed
  - [ ] Benchmark ranking speed
  - [ ] Benchmark answer generation
  - [ ] Target: Full query <5 seconds
  - [ ] Profile to find bottlenecks

- [ ] **Manual Testing**
  - [ ] Test 50+ real queries
  - [ ] Test job search
  - [ ] Test product search
  - [ ] Test event search
  - [ ] Test error cases

- [ ] **Security Testing**
  - [ ] Check for SQL injection
  - [ ] Check authentication
  - [ ] Rate limiting
  - [ ] Input validation

---

## PHASE 5: Documentation & Polish (Week 4)

### ✅ Subtask: Documentation

- [ ] **Code Documentation**
  - [ ] Docstrings on all functions
  - [ ] Type hints everywhere
  - [ ] Comments on complex logic

- [ ] **API Documentation**
  - [ ] OpenAPI/Swagger docs
  - [ ] Update README with new endpoints
  - [ ] Add example requests/responses

- [ ] **Architecture Documentation**
  - [ ] Update architecture diagram
  - [ ] Document data flow
  - [ ] Document decision rationale

- [ ] **User Documentation**
  - [ ] How to use the system
  - [ ] Examples for each use case
  - [ ] Troubleshooting guide

- [ ] **README Updates**
  - [ ] Update main README
  - [ ] Add new features
  - [ ] Update tech stack
  - [ ] Add usage examples

---

## PHASE 5: Deployment (Week 4)

### ✅ Subtask: Production Deployment

- [ ] **Docker & Containerization**
  - [ ] Update Dockerfile with new dependencies
  - [ ] Test Docker build
  - [ ] Test docker-compose up

- [ ] **Environment Configuration**
  - [ ] Update .env template
  - [ ] Document all env variables
  - [ ] Test on staging

- [ ] **CI/CD Pipeline**
  - [ ] Create GitHub Actions workflow
  - [ ] Run tests on push
  - [ ] Build and push image

- [ ] **Deployment Checklist**
  - [ ] All tests passing
  - [ ] Performance targets met
  - [ ] Security checks passed
  - [ ] Documentation complete
  - [ ] Staging tested
  - [ ] Rollback plan prepared

---

## 🎯 Success Criteria (Final)

### Before Launch, Verify:

- [ ] **Functionality**
  - [ ] Can answer general questions (90%+ accuracy)
  - [ ] Can find and rank job listings
  - [ ] Can detect user intent (90%+ accuracy)
  - [ ] Provides proper citations
  - [ ] Shows action prompts

- [ ] **Performance**
  - [ ] Full query completes in <5 seconds
  - [ ] Crawler respectful (rate limiting, robots.txt)
  - [ ] No memory leaks
  - [ ] CPU usage reasonable

- [ ] **Quality**
  - [ ] Unit test coverage >80%
  - [ ] Integration tests pass
  - [ ] Manual testing passes
  - [ ] No known bugs
  - [ ] Code reviewed

- [ ] **Documentation**
  - [ ] All code documented
  - [ ] README complete
  - [ ] API docs updated
  - [ ] User guide written

- [ ] **Security**
  - [ ] No SQL injection
  - [ ] Authentication working
  - [ ] Rate limiting active
  - [ ] Input validation
  - [ ] Error messages don't leak info

---

## 📊 Progress Tracking

### Track With:

- [ ] GitHub issues for each task
- [ ] Project board (Kanban)
- [ ] Daily standup notes
- [ ] Weekly progress report

### Review At:

- [ ] End of each phase
- [ ] Friday demos
- [ ] Weekly retro

---

## 🚀 Final Deployment

Once all checkboxes are complete:

```bash
# 1. Merge PR
git checkout main
git merge feature/searchshield

# 2. Tag release
git tag v1.0.0-searchshield

# 3. Deploy
docker build -t searchshield:v1.0.0 .
docker push searchshield:v1.0.0
# Deploy to production

# 4. Monitor
# Watch logs for errors
# Monitor performance metrics
# Collect user feedback
```

---

## 💡 Tips for Success

1. **Work in small commits** - Don't wait to commit
2. **Write tests first** - TDD helps catch bugs early
3. **Test locally** - Don't push broken code
4. **Document as you go** - Easier than catching up later
5. **Get feedback early** - Show demos often
6. **Celebrate wins** - Each working module is a success!

---

**Total Effort: 106 hours over 4 weeks**

**You've got this! 🚀**
