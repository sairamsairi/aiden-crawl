# Project Structure Analysis: TruthShield AI

## 🗂️ Current Folder Structure

```
crawler-AI/
├── backend/ (FastAPI Python Backend)
│   ├── main.py
│   │   └─ Initializes FastAPI app with 3 routers
│   ├── models.py
│   │   └─ SQLAlchemy models: User, UserHistory
│   ├── database.py
│   │   └─ SQLAlchemy database connection
│   ├── auth.py
│   │   └─ Password hashing, JWT token generation
│   ├── requirements.txt
│   │   └─ Dependencies: FastAPI, Pydantic-AI, Anthropic, Torch, Transformers
│   │
│   ├── routers/ (API Endpoints)
│   │   ├── auth_routes.py
│   │   │   └─ POST /auth/register, POST /auth/login
│   │   ├── detection_routes.py
│   │   │   └─ POST /detect/analyze (Full fact-checking)
│   │   └─ chat_routes.py
│   │       └─ POST /chat/ (Placeholder - not implemented)
│   │
│   ├── services/ (Business Logic)
│   │   ├── fact_checker_service.py
│   │   │   └─ FactCheckingService wrapper (async/sync)
│   │   └─ email_service.py
│   │       └─ Send welcome emails
│   │
│   ├── fact_checker/ (Multi-Agent Orchestration)
│   │   ├── __init__.py
│   │   ├── llm.py
│   │   │   └─ build_model() - LLM configuration
│   │   ├── claim_extractor_agent.py
│   │   │   ├─ Extracts claims from text
│   │   │   └─ Classes: Claim, ClaimsExtraction
│   │   ├── evidence_agent.py
│   │   │   ├─ Plans verification searches
│   │   │   ├─ Searches for evidence (DuckDuckGo)
│   │   │   └─ Classes: VerificationItem, VerificationPlan
│   │   ├── verdict_generator.py
│   │   │   ├─ Generates fact-check verdicts
│   │   │   └─ Classes: ClaimVerdict, FactCheckReport
│   │   └─ fact_checker_orchestrator.py
│   │       ├─ FactChecker class (Main coordinator)
│   │       └─ Manages full pipeline:
│   │           1. Extract claims
│   │           2. Plan verification
│   │           3. Search evidence
│   │           4. Generate verdict
│   │
│   ├── FACT_CHECKER_GUIDE.md
│   │   └─ Documentation of fact-checking pipeline
│   └─ Dockerfile
│       └─ Container setup
│
├── frontend/ (React UI)
│   ├── public/
│   ├── src/
│   │   ├── index.js
│   │   ├── App.js
│   │   │   └─ Main app with Auth/Dashboard routing
│   │   ├── App.css
│   │   ├── api.js
│   │   │   └─ API client functions
│   │   └─ components/
│   │       ├── Auth.js
│   │       │   └─ Login & Registration UI
│   │       ├── Dashboard.js
│   │       │   ├─ Main interface
│   │       │   ├─ Text input (paste news)
│   │       │   ├─ Analyze button
│   │       │   └─ Shows analysis progress + results
│   │       └─ Result.js
│   │           └─ Displays fact-check results
│   └── package.json
│       └─ React dependencies
│
└── github/
    └── workflows/
        └─ CI/CD pipeline (empty/placeholder)
```

---

## 📊 Code Statistics

### Backend Modules

| Module                       | Lines            | Purpose                             |
| ---------------------------- | ---------------- | ----------------------------------- |
| main.py                      | 20               | FastAPI app initialization          |
| models.py                    | 20               | Database models (User, UserHistory) |
| auth.py                      | 80               | Authentication utilities            |
| database.py                  | 20               | Database connection                 |
| auth_routes.py               | 60               | User registration/login endpoints   |
| detection_routes.py          | 80               | Fact-checking endpoint              |
| chat_routes.py               | 20               | Chat placeholder                    |
| llm.py                       | 30               | LLM configuration                   |
| claim_extractor_agent.py     | 100              | Claim extraction                    |
| evidence_agent.py            | 150              | Evidence gathering & search         |
| verdict_generator.py         | 120              | Verdict generation                  |
| fact_checker_orchestrator.py | 150              | Pipeline orchestration              |
| fact_checker_service.py      | 50               | Service wrapper                     |
| email_service.py             | 30               | Email sending                       |
| **TOTAL BACKEND**            | **~1,000 lines** |                                     |

### Frontend Components

| Component          | Lines          | Purpose                      |
| ------------------ | -------------- | ---------------------------- |
| App.js             | 30             | Main routing                 |
| Auth.js            | 80             | Login/registration UI        |
| Dashboard.js       | 120            | Main interface & analysis UI |
| Result.js          | 60             | Results display              |
| api.js             | 40             | API client                   |
| **TOTAL FRONTEND** | **~330 lines** |                              |

**Total Project: ~1,330 lines of code**

---

## 🔄 Data Flow

### Current: Fact-Checking Pipeline

```
┌─────────────────────────────────────────┐
│           User Input (Text)             │
└────────────────┬────────────────────────┘
                 │
                 ↓
         ┌───────────────────┐
         │ Claim Extractor   │ → Extract verifiable claims
         └────────┬──────────┘
                  │
                  ↓ [Claim data]
         ┌────────────────────┐
         │ Fact Planner       │ → Plan search queries
         └────────┬───────────┘
                  │
                  ↓ [Search queries]
         ┌────────────────────┐
         │ Evidence Searcher  │ → Search DuckDuckGo
         └────────┬───────────┘
                  │
                  ↓ [Evidence data]
         ┌────────────────────┐
         │ Verdict Agent      │ → Generate verdicts
         └────────┬───────────┘
                  │
                  ↓ [FactCheckReport]
     ┌────────────────────────────┐
     │ JSON Response to Frontend  │
     └────────────────────────────┘
```

### Database Flow

```
User Registration/Login
    ↓
    └─→ users table (email, password)

User analyzes text
    ↓
    └─→ user_history table (stores results)

Future: Search results caching
    ↓
    └─→ search_results table (new - needed)

Future: Job tracking
    ↓
    └─→ job_applications table (new - needed)
```

---

## 🔌 API Endpoints Summary

### Currently Implemented ✅

```
POST /auth/register
├─ Input: {email, password}
└─ Output: {message}

POST /auth/login
├─ Input: {username (email), password}
└─ Output: {access_token, token_type}

POST /detect/analyze
├─ Input: {text}
├─ Process: Fact-check pipeline
└─ Output: {FactCheckReport with verdicts}

GET /
└─ Output: {message: "TruthShield AI running"}
```

### Placeholder ⏳

```
POST /chat/
├─ Currently returns: "Hello from TruthShield GPT"
└─ Needs: Actual chat logic
```

---

## 🧠 Agent Architecture

### Current Agents (4)

```
ClaimExtractorAgent
├─ System: Fact-checking specialist
├─ Input: Any text/article
├─ Output: ClaimsExtraction (list of Claim objects)
└─ Model: Anthropic/Cohere LLM

FactPlannerAgent
├─ System: Fact-checking specialist
├─ Input: Individual claim text
├─ Output: VerificationPlan (search queries)
└─ Model: Anthropic/Cohere LLM

EvidenceSearcherAgent
├─ System: Evidence gathering
├─ Input: Search query
├─ Tool: DuckDuckGo API (duckduckgo_search_tool)
├─ Output: Search results + snippets
└─ Model: Anthropic/Cohere LLM

VerdictAgent
├─ System: Fact-checking expert
├─ Input: Text + evidence
├─ Output: FactCheckReport (verdicts + scores)
└─ Model: Anthropic/Cohere LLM
```

---

## 💾 Database Schema

### Current Tables (2)

```
users
├─ id (PK)
├─ email (UNIQUE)
└─ password (hashed)

user_history
├─ id (PK)
├─ user_id (FK)
├─ input_text
└─ result (JSON string)
```

---

## 🔐 Authentication Flow

```
User enters email/password
    ↓
POST /auth/register
    ├─ Hash password with bcrypt
    ├─ Store in users table
    └─ Send welcome email

OR

POST /auth/login
    ├─ Verify password
    ├─ Generate JWT token
    └─ Return access token

Subsequent requests
    ├─ Include token in Authorization header
    ├─ get_current_user() validates token
    └─ Access protected endpoints
```

---

## 🏗️ Tech Stack Details

### Backend

```
Framework:      FastAPI (async web framework)
ORM:            SQLAlchemy 2.0.23
Validation:     Pydantic v2
AI/Agents:      Pydantic-AI 0.9.0
LLMs:           Anthropic (primary), Cohere (fallback)
Search:         DuckDuckGo API
ML:             PyTorch 2.0, Transformers 4.40
Auth:           JWT (python-jose), bcrypt
Server:         Uvicorn
Logging:        Logfire
Email:          (email_service.py - basic)
Database:       SQLAlchemy with SQLite/PostgreSQL
```

### Frontend

```
Framework:      React 19.2.4
Build:          Create React App (react-scripts 5.0)
Testing:        Jest + React Testing Library
HTTP Client:    Fetch API (in api.js)
State:          React hooks (useState)
```

### Infrastructure

```
Containerization:   Docker (Dockerfile present)
Environment:        .env file support
CORS:               Enabled for all origins
Rate Limiting:      Not implemented (needed)
```

---

## 🔄 Current Capabilities Matrix

| Capability           | Implemented | Code Location                         |
| -------------------- | ----------- | ------------------------------------- |
| User Registration    | ✅          | auth_routes.py                        |
| User Login           | ✅          | auth_routes.py                        |
| Text Input           | ✅          | frontend/Dashboard.js                 |
| Claim Extraction     | ✅          | fact_checker/claim_extractor_agent.py |
| Web Search           | ✅          | fact_checker/evidence_agent.py        |
| Verdict Generation   | ✅          | fact_checker/verdict_generator.py     |
| Result Display       | ✅          | frontend/Result.js                    |
| Error Handling       | ✅          | Fallback mechanisms in all agents     |
| Authentication       | ✅          | auth.py + auth_routes.py              |
| Database Persistence | ✅          | models.py + database.py               |

---

## 🚨 Missing Capabilities

| Capability            | Needed     | Code Location             |
| --------------------- | ---------- | ------------------------- |
| Web Crawling          | ❌         | (backend/crawler/)        |
| Intent Classification | ❌         | (backend/agents/)         |
| Result Ranking        | ❌         | (backend/ranking/)        |
| Job Search            | ❌         | (backend/integrations/)   |
| Action Handling       | ❌         | (backend/agents/)         |
| Query Input (UI)      | ❌         | (frontend/components/)    |
| Result Cards          | ❌         | (frontend/components/)    |
| Job Listings (UI)     | ❌         | (frontend/components/)    |
| Citations             | ⚠️ Partial | (Result.js needs upgrade) |

---

## 📦 Dependency Tree

```
Core Dependencies
├─ FastAPI → Uvicorn, Starlette, Pydantic
├─ SQLAlchemy → Database abstraction
├─ Pydantic-AI → Agent orchestration
│   └─ Requires: LLM provider (Anthropic/Cohere)
├─ PyTorch → ML computations
├─ Transformers → Hugging Face models
├─ python-jose → JWT tokens
├─ bcrypt → Password hashing
└─ python-dotenv → Environment variables

Search Dependencies
├─ ddgs → DuckDuckGo search
└─ requests → HTTP requests

Frontend Dependencies
├─ React → UI framework
└─ React-DOM → React rendering

Logging & Monitoring
└─ logfire → Monitoring service
```

---

## 🎯 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │     Auth     │  │  Dashboard   │  │   Result     │      │
│  │   (Login)    │  │  (Text Input)│  │ (Display)    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────────┬──────────────────────────────────────┘
                         │ HTTP/REST API
┌────────────────────────↓──────────────────────────────────────┐
│                    BACKEND (FastAPI)                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                API Routers                           │   │
│  │  ┌─────────────┐ ┌────────────┐ ┌─────────────────┐ │   │
│  │  │ auth_routes │ │detect_routes│ │ chat_routes   │ │   │
│  │  └─────────────┘ └────────────┘ └─────────────────┘ │   │
│  └──────────────┬───────────────────────────────────────┘   │
│                 │                                             │
│  ┌──────────────↓───────────────────────────────────────┐   │
│  │          Services Layer                             │   │
│  │  ┌──────────────────────┐  ┌──────────────────────┐ │   │
│  │  │ FactCheckingService  │  │   EmailService       │ │   │
│  │  └──────────────────────┘  └──────────────────────┘ │   │
│  └──────────────┬───────────────────────────────────────┘   │
│                 │                                             │
│  ┌──────────────↓───────────────────────────────────────┐   │
│  │     Multi-Agent Orchestration (fact_checker/)       │   │
│  │  ┌──────────────┐   ┌──────────────┐               │   │
│  │  │ ClaimExtractor│  │ FactPlanner   │               │   │
│  │  └──────────────┘   └──────────────┘               │   │
│  │  ┌──────────────┐   ┌──────────────┐               │   │
│  │  │ Evidence     │   │ Verdict      │               │   │
│  │  │ Searcher     │   │ Generator    │               │   │
│  │  └──────────────┘   └──────────────┘               │   │
│  └──────────────┬───────────────────────────────────────┘   │
│                 │                                             │
│  ┌──────────────↓───────────────────────────────────────┐   │
│  │     External Services                               │   │
│  │  ┌──────────────┐   ┌──────────────┐               │   │
│  │  │ DuckDuckGo   │   │ LLM Provider │               │   │
│  │  │ Search API   │   │ (Anthropic)  │               │   │
│  │  └──────────────┘   └──────────────┘               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Database (SQLAlchemy)                   │   │
│  │  ┌──────────────┐   ┌──────────────────┐           │   │
│  │  │ users table  │   │ user_history     │           │   │
│  │  │              │   │ table            │           │   │
│  │  └──────────────┘   └──────────────────┘           │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Deployment Setup

### Current

- ✅ Dockerfile present
- ✅ Docker-compose.yaml present
- ✅ Environment variables (.env)
- ✅ CORS configured
- ❌ No CI/CD pipeline (empty github/workflows/)

### Files

```
Dockerfile
├─ FROM python:3.11
├─ WORKDIR /app
├─ COPY requirements.txt
├─ RUN pip install
├─ COPY . .
└─ CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]

docker-compose.yaml
├─ Services: backend, frontend
├─ Ports: 8000 (backend), 3000 (frontend)
└─ Network: internal

.env
├─ LLM_API_KEYS
├─ Database credentials
└─ Environment mode
```

---

## ✅ Summary

**What Works**: Solid multi-agent fact-checking system with modern stack  
**What's Missing**: Web crawling, intent detection, ranking, actions  
**Quality**: ~1,300 lines of well-structured code  
**Ready for**: Adding 5 new modules to reach 100% feature parity

---

**Next**: See IMPLEMENTATION_PLAN.md for how to build missing modules!
