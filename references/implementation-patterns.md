# Implementation Patterns for Work Systems

## Introduction

This guide presents common architectural patterns for work systems. Use these patterns to guide technical implementation decisions during spec creation.

**How to use this guide:**
- Choose a pattern based on your requirements (scale, complexity, team skills)
- Each pattern includes: when to use, technology examples, pros/cons, complexity level
- Patterns can be combined (e.g., local-first with cloud sync)

---

## Pattern 1: Local-First

### Description

All data stored locally on user's machine. No server, no cloud dependencies. Application runs entirely offline.

### When to Use

- **Single user** systems (no collaboration needed)
- **Privacy sensitive** data (don't want cloud storage)
- **Simple requirements** (no integrations, no multi-device access)
- **Fast performance** needs (local access is fastest)
- **Minimal ops overhead** (no servers to maintain)

### Technology Stack Examples

**Lightweight (CLI or desktop app)**:
- **Language**: Python, Node.js, Go
- **Storage**: SQLite, JSON files, CSV files
- **Interface**: CLI (Click, Commander), Desktop app (Electron, Tauri)
- **Deployment**: Single executable or pip/npm install

**Example**: Personal task tracker (see [task-management-spec.md](./examples/task-management-spec.md))

### Architecture

```
User Machine
├── Application Binary (CLI or Desktop App)
├── Local Database (SQLite at ~/.app/data.db)
├── Config File (~/.app/config.json)
└── Logs (~/.app/logs/)
```

### Pros

✓ **Fast**: No network latency, instant operations
✓ **Private**: Data never leaves machine
✓ **Offline**: Works without internet
✓ **Simple**: No backend, no deployment, no auth
✓ **Low cost**: No cloud bills
✓ **Easy backup**: Copy one directory

### Cons

✗ **Single device**: Can't access from other machines (unless you manually sync files)
✗ **No collaboration**: One user only
✗ **No web access**: Must install app
✗ **Backup responsibility**: User must remember to backup
✗ **Limited integrations**: Can't easily connect to cloud services

### Complexity Level

**Low** - Perfect for beginners or solo projects. Minimal moving parts.

### Migration Path

Start local-first, add cloud sync later if needed:
- Keep SQLite as local cache
- Add sync service (Dropbox, iCloud, custom API)
- Implement conflict resolution

---

## Pattern 2: Client-Server

### Description

Traditional web application with frontend, backend API, and database. Multi-user, accessible from any device with browser.

### When to Use

- **Multi-user** systems (team collaboration)
- **Web access** required (no app install)
- **Real-time updates** needed (multiple users seeing same data)
- **Complex workflows** (state machines, approval gates)
- **Integrations** with other services (APIs, webhooks)
- **Centralized control** (admin can manage all data)

### Technology Stack Examples

**Modern stack**:
- **Frontend**: React/Next.js, Vue/Nuxt, Svelte/SvelteKit
- **Backend**: Node.js (Express, Fastify), Python (FastAPI, Django), Go (Gin, Echo)
- **Database**: PostgreSQL, MySQL, MongoDB
- **Auth**: OAuth (Okta, Auth0), JWT, Session cookies
- **Hosting**: Vercel/Netlify (frontend), Railway/Render/Fly.io (backend), Supabase/PlanetScale (DB)

**Example**: Team knowledge base (see [knowledge-management-spec.md](./examples/knowledge-management-spec.md))

### Architecture

```
Client (Browser)
↓ HTTPS
API Server (REST or GraphQL)
↓
Database (PostgreSQL)
↓
Integrations (Slack, Email, etc.)
```

### Pros

✓ **Multi-user**: Team collaboration built-in
✓ **Multi-device**: Access from any browser
✓ **Centralized**: Single source of truth
✓ **Rich UI**: Full web app capabilities
✓ **Integrations**: Easy to connect external services
✓ **Scalable**: Can handle growth (with proper architecture)

### Cons

✗ **Complex**: More moving parts (frontend, backend, database, deployment)
✗ **Requires internet**: No offline mode (without PWA)
✗ **Higher cost**: Cloud hosting, database, CI/CD
✗ **Auth needed**: Must handle user authentication and authorization
✗ **Ops overhead**: Monitoring, updates, backups

### Complexity Level

**Medium to High** - Requires full-stack skills, DevOps knowledge, and ongoing maintenance.

### Variants

**Serverless Client-Server**:
- Use serverless functions (AWS Lambda, Vercel Functions, Cloudflare Workers)
- Reduces ops overhead, pay per request
- Good for variable traffic

**Monolithic vs. Microservices**:
- **Monolith**: Single codebase for backend (simpler, start here)
- **Microservices**: Separate services per domain (complex, only for large scale)

---

## Pattern 3: Event-Driven

### Description

Work enters as events (emails, webhooks, messages). System processes events asynchronously through queues and workers. No direct user interface—automation-focused.

### When to Use

- **Automation workflows** (no human in the loop for most operations)
- **High volume** (1000s of events per day)
- **Asynchronous processing** (work doesn't need immediate response)
- **Integration-heavy** (connecting multiple external systems)
- **Reliability critical** (need retry logic, error handling)

### Technology Stack Examples

**Cloud-native**:
- **Event Source**: AWS SES (email), Webhooks, Pub/Sub topics
- **Queue**: AWS SQS, Google Pub/Sub, RabbitMQ, Redis Streams
- **Workers**: AWS Lambda, Google Cloud Functions, background jobs (Celery, Bull)
- **Database**: DynamoDB, Firestore, PostgreSQL
- **Orchestration**: AWS Step Functions, Temporal, Airflow

**Example**: Email to ticket automation (see [automation-workflow-spec.md](./examples/automation-workflow-spec.md))

### Architecture

```
Event Source (Email, Webhook)
↓
Message Queue (SQS, Pub/Sub)
↓
Worker/Lambda (Process event)
↓
Database (Store result)
↓
Downstream System (Linear, Slack, etc.)
```

### Pros

✓ **Scalable**: Handle bursts of traffic (queue buffers load)
✓ **Reliable**: Retry failed events automatically
✓ **Decoupled**: Components can fail independently
✓ **Asynchronous**: Don't block on slow operations
✓ **Cost-efficient**: Pay per event (serverless)

### Cons

✗ **Complex debugging**: Distributed tracing needed
✗ **Eventual consistency**: Data may not be immediately updated everywhere
✗ **No UI** (by default): Need separate dashboard for monitoring
✗ **Vendor lock-in** (if using cloud services heavily)
✗ **Learning curve**: Event-driven patterns are less intuitive

### Complexity Level

**High** - Requires understanding of distributed systems, queues, idempotency, and error handling.

### Key Concepts

**Idempotency**: Processing same event multiple times produces same result (important for retries)
**Dead Letter Queue (DLQ)**: Where failed events go after max retries
**Circuit Breaker**: Stop calling failing external service to prevent cascade failures

---

## Pattern 4: Hybrid (Local + Cloud Sync)

### Description

Local-first application with cloud sync for multi-device access. Best of both worlds: fast local access + cloud backup + cross-device sync.

### When to Use

- **Single user, multiple devices** (laptop, phone, tablet)
- **Offline-first** (must work without internet)
- **Performance critical** (local is faster than cloud queries)
- **Data ownership** (user wants local copy, not just cloud)
- **Gradual adoption** (start local, add cloud later)

### Technology Stack Examples

**Desktop/Mobile with Cloud Sync**:
- **Frontend**: Electron, React Native, Flutter
- **Local Storage**: SQLite, IndexedDB, Realm
- **Cloud Sync**: Custom API, Firestore, PouchDB + CouchDB, Supabase
- **Conflict Resolution**: CRDTs, operational transform, last-write-wins

**Example**: Note-taking app (Obsidian model), todo app (Todoist model)

### Architecture

```
Device 1 (Laptop)
├── Local SQLite
└── Sync Service → Cloud DB

Device 2 (Phone)
├── Local SQLite
└── Sync Service → Cloud DB

Cloud DB (Single source of truth)
```

### Pros

✓ **Fast**: Local reads/writes, instant response
✓ **Offline**: Works without internet
✓ **Multi-device**: Sync across devices
✓ **Resilient**: Local copy even if cloud is down
✓ **User control**: Data on their machine, not just cloud

### Cons

✗ **Sync complexity**: Conflict resolution is hard
✗ **Storage duplication**: Data stored locally + cloud
✗ **Higher development cost**: Build local + cloud + sync logic
✗ **Versioning**: Need to handle schema migrations across devices

### Complexity Level

**High** - Sync is deceptively difficult. Conflicts, partial syncs, and schema changes add complexity.

### Sync Strategies

**Full Sync**: Download entire dataset on each sync (simple, works for small datasets)
**Delta Sync**: Only sync changes since last sync (efficient, more complex)
**Operational Transform**: Sync at operation level, resolve conflicts (most complex, most powerful)

---

## Choosing a Pattern: Decision Tree

Use this flowchart to choose the right pattern:

### Start Here

**Q1: Is this single-user or multi-user?**
- **Single user** → Q2
- **Multi-user** → Q4

### Q2: Do you need multi-device access?
- **No** (laptop only) → **Local-First** ✓
- **Yes** (laptop + phone) → Q3

### Q3: Can you tolerate occasional sync conflicts?
- **Yes** → **Hybrid (Local + Cloud)** ✓
- **No** (need single source of truth) → **Client-Server** ✓

### Q4: Is this primarily automation or human-driven?
- **Automation** (no UI) → **Event-Driven** ✓
- **Human-driven** (people interact) → Q5

### Q5: Is this real-time collaboration (Google Docs style)?
- **Yes** → **Client-Server** with WebSockets ✓
- **No** (async collaboration fine) → **Client-Server** ✓

---

## Combining Patterns

Patterns can be combined for complex systems:

### Example 1: Client-Server + Event-Driven

**Use case**: Team dashboard with automated data ingestion

**Architecture**:
- **Client-Server**: Web UI for team to view/manage work
- **Event-Driven**: Background workers ingest data from APIs, emails, webhooks
- **Shared Database**: Both UI and workers read/write same database

**Example**: Support ticket system with email automation (client-server UI + event-driven email parsing)

### Example 2: Local-First + Event-Driven

**Use case**: Personal automation tool that triggers cloud workflows

**Architecture**:
- **Local-First**: CLI tool on user's machine
- **Event-Driven**: When user runs command, sends event to cloud queue → triggers workflow
- **Hybrid**: Local state + cloud execution

**Example**: `deploy` CLI tool that triggers cloud build + deployment pipeline

### Example 3: Client-Server + Local Caching

**Use case**: Web app that works offline

**Architecture**:
- **Client-Server**: Primary mode when online
- **Local-First**: Progressive Web App (PWA) with IndexedDB cache for offline mode
- **Sync**: When back online, sync local changes to server

**Example**: Mobile-first CRM app for field sales reps (often offline)

---

## Technology Recommendations by Scale

### Small Scale (1-10 users, <1000 items/day)

**Recommended**: Local-First or Simple Client-Server

**Stack**:
- SQLite or JSON files
- CLI or simple web UI (Flask, Express + vanilla JS)
- No queue (process synchronously)
- Manual deployment (VPS, Heroku)

**Why**: Simplicity > scalability at small scale. Avoid over-engineering.

### Medium Scale (10-100 users, 1000-10000 items/day)

**Recommended**: Client-Server

**Stack**:
- PostgreSQL or MongoDB
- Modern frontend framework (React, Vue)
- REST or GraphQL API
- Background job queue (Redis + Bull, Celery)
- Platform deployment (Railway, Render, Fly.io)

**Why**: Need multi-user, but manageable complexity. Platform services handle ops.

### Large Scale (100+ users, 10000+ items/day)

**Recommended**: Client-Server + Event-Driven

**Stack**:
- PostgreSQL with read replicas
- Frontend on CDN (Vercel, Cloudflare)
- Microservices or modular monolith
- Message queue (SQS, Pub/Sub, Kafka)
- Serverless workers (Lambda, Cloud Functions)
- Kubernetes or managed container service

**Why**: Need scalability, reliability, and performance. Justify complexity with scale.

---

## Common Mistakes to Avoid

### 1. Over-Engineering Early

**Mistake**: Building microservices + Kubernetes + event sourcing for 5 users

**Solution**: Start simple (Local-First or monolithic Client-Server). Refactor when you have real scale problems.

### 2. Under-Estimating Sync Complexity

**Mistake**: "I'll just add sync later" → Rewrites entire app because local schema incompatible with cloud

**Solution**: If you think you'll need multi-device, start with Client-Server (server is source of truth). Only use Hybrid if offline-first is critical.

### 3. Choosing Event-Driven for Low Volume

**Mistake**: AWS Lambda + SQS + DynamoDB for 10 emails/day

**Solution**: Simple script with cron job is fine for low volume. Use Event-Driven when volume is high (1000s/day) or unpredictable.

### 4. No Auth on "Internal Tools"

**Mistake**: Building team tool without authentication "because it's just for us"

**Solution**: Always add auth for multi-user tools. Okta SSO, Google OAuth, or simple username/password. Security first.

### 5. Ignoring Backups

**Mistake**: Local-First app with no backup strategy → User loses laptop → All data gone

**Solution**: For Local-First, provide export command (`myapp export backup.json`). For Client-Server, automated daily DB backups.

---

## Summary Table

| Pattern | Users | Scale | Complexity | Cost | Offline | Best For |
|---------|-------|-------|------------|------|---------|----------|
| **Local-First** | 1 | Low | Low | $0 | ✓ Yes | Personal tools, privacy-focused |
| **Client-Server** | Many | Med-High | Medium | $$-$$$ | ✗ No | Team collaboration, web apps |
| **Event-Driven** | N/A | High | High | $$ | ✗ No | Automation, integrations, high volume |
| **Hybrid** | 1 | Low-Med | High | $$ | ✓ Yes | Multi-device, offline-first |

---

## Additional Resources

- **Local-First Software**: [https://www.inkandswitch.com/local-first/](https://www.inkandswitch.com/local-first/)
- **Event-Driven Architecture**: [AWS Event-Driven Patterns](https://serverlessland.com/patterns)
- **Sync Strategies**: [Conflict-Free Replicated Data Types (CRDTs)](https://crdt.tech/)

---

This guide provides a starting point for architectural decisions. During the interview, use these patterns to discuss tradeoffs and help users choose the right approach for their work system.
