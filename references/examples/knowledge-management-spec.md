# TeamKnowledge - Engineering Team Wiki System

## Overview

- **Purpose**: Centralized knowledge base for engineering team to capture decisions, docs, and tribal knowledge with AI-powered search and recommendations
- **Last Updated**: 2026-01-13
- **Status**: Ready for Implementation

## System Scope

### In Scope

- Capture articles, docs, runbooks, decisions (ADRs), meeting notes
- Multiple entry points: web form, Slack bot, API
- Category-based organization with tagging
- Full-text search with AI-powered semantic search
- Recommend related articles when viewing
- Version history for articles
- Integration with Slack for notifications and quick lookup
- Role-based access (engineers, managers, all-company)

### Explicitly Out of Scope (Non-Goals)

- NOT replacing Notion or Confluence for project management (this is reference docs only)
- NOT a real-time collaboration editor (use Google Docs for draft writing, publish here when stable)
- NOT handling code documentation (use docstrings and generated API docs for that)
- NOT providing user training or onboarding flows (just documentation storage and retrieval)

## User Profiles

### Primary Users

- **Engineers** (20 people): Create and read articles. Daily active users looking up runbooks, past decisions, system architecture docs.
- **Engineering Managers** (3 people): Create decisions/updates, read reports, approve sensitive content. Several times per week.
- **All Company** (100 people): Read-only access to public articles (onboarding, policies). Occasional use.

### Technical Level

**Intermediate** - Engineers comfortable with markdown, web interfaces, Slack bots. Managers comfortable with web dashboards. Non-engineers expect simple read-only web interface with search.

## Work Flow

### Input & Capture

#### Entry Points

- **Web Form**: Primary interface at `knowledge.company.internal` for creating/editing articles. Markdown editor with preview.
- **Slack Bot**: `/knowledge add [title]` opens web form pre-filled with title. Quick capture during discussions.
- **API**: POST /api/articles for automated doc generation (e.g., from CI/CD publishing weekly metrics)
- **Import**: Bulk import from existing Confluence via CSV or API (migration tool)

#### Required Metadata

- **Title** (required, text, user-provided): Article name
- **Content** (required, markdown, user-provided): Article body
- **Category** (required, dropdown, user-selected): Engineering/Product/Operations/Culture/Policy
- **Tags** (optional, multi-select or free-text, user-provided): Additional labels
- **Visibility** (required, dropdown, user-selected): Public/Team-Only/Managers-Only
- **Author** (required, email, auto-captured from auth): Who created it
- **Created/Updated** (required, timestamp, auto): When created and last edited
- **Status** (required, enum, user-set): Draft/Published/Archived

#### Work Types

All content treated as "articles" but categorized by type:
- **Runbook**: Operational procedures (e.g., "How to restart production database")
- **Architecture Decision Record (ADR)**: Why we chose X over Y
- **Meeting Notes**: Team discussions and action items
- **Reference Doc**: General knowledge (e.g., "API authentication guide")
- **Announcement**: Company-wide updates (e.g., "New parental leave policy")

## Work Flow

### Processing & Organization

#### Categorization Logic

- **Manual Category Selection**: User chooses from predefined list on creation
- **Auto-tag Suggestions**: AI analyzes content and suggests 3-5 tags based on keywords and similarity to existing articles
- **User Confirmation**: User can accept/reject/modify suggested tags

#### Priority Framework

No priority system - all articles equal. Relevance determined by:
- Recency (newer articles ranked higher in search)
- View count (popular articles surface more)
- Semantic similarity to search query

#### Workflow States

1. **Draft**: Author writing, not visible to others
2. **Published**: Live and searchable by users with appropriate access
3. **Archived**: Outdated but retained for history, marked with banner "This article is outdated. See [link] for current version."

Transitions:
- Draft → Published: Author clicks "Publish" button
- Published → Archived: Author or manager clicks "Archive" button, must provide reason

#### Automation Rules

- **Auto-tag Suggestions**: On save draft, Claude API analyzes content and suggests tags based on topic modeling
- **Related Article Links**: When viewing article, AI finds 5 most semantically similar articles and shows "Related Reading" sidebar
- **Stale Content Detector**: Weekly cron job finds articles >1 year old with no updates, tags with `needs-review`, notifies author
- **Slack Notifications**: When article published in categories user is watching, send Slack DM with title and link

### Output & Interaction

#### User Interface

- **Primary**: Web app at `knowledge.company.internal`
  - **Home**: Recently updated articles, most viewed, categories
  - **Search**: Full-text + semantic search bar prominent on every page
  - **Article View**: Markdown rendered, table of contents, related articles sidebar, edit button (if author or manager)
  - **Category Browse**: List articles by category, filterable by tags
  - **Profile**: My articles, my drafts, articles I'm watching

- **Secondary**: Slack bot
  - `/knowledge search [query]` - Returns top 3 results with snippets
  - `/knowledge random` - Show random article (discover hidden gems)
  - Notifications for watched categories

- **API**: REST API for programmatic access (read-only for most, write for admins)

#### Key Actions

- **Create Article**: Draft → Edit → Publish workflow
- **Edit Article**: Edit button on article view (author or manager only). Creates new version, keeps history.
- **Search**: Full-text search across titles and content. Semantic search using embeddings for "fuzzy" topic matching.
- **Browse Categories**: Filter by category and tags
- **Watch Category**: Get notifications when articles published in category
- **Archive**: Mark outdated with reason, show banner on article
- **View History**: See past versions of article with diff view

#### Notifications/Alerts

- **New Article in Watched Category**: Slack DM with title and link, within 5 minutes of publication
- **Stale Content**: Email to author when article >1 year old, prompt to review/update or archive
- **Edit by Others**: If someone edits your article, get Slack DM with summary of changes
- **Digest**: Optional weekly email with "Top 5 Articles This Week" based on views

## Technical Architecture

### Technology Stack

- **Frontend**: Next.js 14 with TypeScript, Tailwind CSS, deployed to Vercel
- **Backend**: Node.js 20 with Express, deployed to Railway
- **Database**: PostgreSQL 15 on Supabase (articles, users, tags, versions)
- **Vector Database**: Pinecone for article embeddings (semantic search)
- **AI**: Claude API (Anthropic) for tag suggestions and summarization
- **Search**: PostgreSQL full-text search + Pinecone vector search
- **Auth**: Okta SSO (company-wide identity provider)
- **Slack**: Bolt framework for Node.js for bot
- **File Storage**: S3 for article attachments/images

### Data Model

**articles**
- id, title, content_markdown, category, visibility, status, author_id, created_at, updated_at, view_count
- Has many tags (many-to-many via article_tags)
- Has many versions (one-to-many)
- Belongs to one user (author)

**users**
- id, email, name, role (engineer|manager|all_company), created_at
- Has many articles (as author)
- Has many watched_categories

**tags**
- id, name, created_at
- Has many articles (many-to-many via article_tags)

**article_versions**
- id, article_id, content_markdown, version_number, changed_by_user_id, changed_at, change_summary
- Belongs to one article

**article_embeddings**
- article_id, embedding_vector (stored in Pinecone, not PostgreSQL)

### AI/Automation Components

**Auto-tag Suggestions**
- **Purpose**: Suggest relevant tags based on content analysis
- **Model**: Claude 3.5 Sonnet via Anthropic API
- **Input**: Article title + first 500 words of content
- **Output**: List of 3-5 suggested tags with relevance scores
- **Threshold**: Show suggestions to user, no auto-application (user confirms)
- **Fallback**: If API fails, skip suggestions (user manually tags)
- **Cost**: ~$0.02 per article (acceptable for 5-10 articles/day)

**Semantic Search**
- **Purpose**: Find articles by meaning, not just keywords
- **Model**: OpenAI text-embedding-3-small (cheaper than Claude embeddings)
- **Process**: On publish, generate embedding → store in Pinecone → index for search
- **Query**: User search → generate query embedding → find top-K similar articles
- **Hybrid**: Combine full-text results + semantic results, weighted 40/60
- **Cost**: ~$0.0001 per article embedding, ~$0.0001 per search (negligible)

**Related Articles**
- **Purpose**: Recommend similar articles when viewing
- **Logic**: Use Pinecone to find 5 most similar embeddings to current article
- **Filtering**: Exclude archived articles, respect visibility permissions
- **Caching**: Cache related articles for 24 hours (embeddings don't change often)

## Edge Cases & Error Handling

**Scenario 1: User edits article but doesn't have permission (not author or manager)**
- **Handling**: Edit button hidden for non-permitted users. If someone bypasses (API call), return 403 Forbidden with message "Only article author or managers can edit."

**Scenario 2: Claude API timeout during tag suggestion**
- **Handling**: Wait 10 seconds for response. If timeout, skip suggestions and show notice: "Auto-tag suggestions unavailable. Please add tags manually."

**Scenario 3: Duplicate article titles**
- **Handling**: Allow duplicates but warn: "An article with this title already exists. Continue anyway?" Link to existing article.

**Scenario 4: User searches but vector database (Pinecone) is down**
- **Handling**: Fallback to PostgreSQL full-text search only. Show notice: "Using basic search (semantic search temporarily unavailable)."

**Scenario 5: Archived article receives many views (still referenced elsewhere)**
- **Handling**: Show banner: "This article is archived and may be outdated. Last updated [date]." Suggest newer articles in same category.

**Scenario 6: Bulk import fails midway (e.g., CSV has errors after row 50)**
- **Handling**: Transaction per article (not batch transaction). Successfully imported articles are saved. Failed articles logged with reasons. Show summary: "Imported 45/100 articles. 55 failed (see error log)."

## Security & Privacy Considerations

**Data Sensitivity**
- Articles may contain internal architecture details, security practices, salary info (managers-only)
- Some articles are public (company policies, onboarding)

**Access Control**
- **Engineers**: Read all Team-Only and Public articles. Write own articles.
- **Managers**: Read all articles including Managers-Only. Write/edit any article in team.
- **All Company**: Read Public articles only.
- Implemented via: Okta SSO roles synced to user.role field. API checks permissions on every request.

**Data Protection**
- All data encrypted at rest (Supabase native encryption)
- All connections use TLS 1.3
- API keys in environment variables, rotated quarterly
- Article history retained indefinitely (for audit trail)

**Compliance**
- No GDPR concerns (employee data, not customer data)
- Audit log for all edits and access to Managers-Only articles

**Backups**
- Supabase automated daily backups (retained 30 days)
- Weekly full database export to S3 for disaster recovery

## Success Metrics

### Primary Metric

**Knowledge Retrieval Success Rate**: % of searches that result in user clicking on an article and spending >1 minute reading it.
- **Target**: >70% (currently people ask teammates or dig through Slack, success rate unknown but low)
- **Measurement**: Track search → click-through → time-on-page. Query analytics database.

### Secondary Metrics

- **Articles Created per Month**: Measure adoption. Target: 20+ articles/month (team of 20 engineers)
- **Slack Bot Usage**: /knowledge search commands per week. Target: 50+ (daily usage)
- **Stale Content Rate**: % of articles >1 year old. Target: <20% (keep content fresh)
- **Search Query Success**: % of searches with 0 results. Target: <10% (good coverage)

### Failure Indicators

- **Low article creation**: <5 articles/month → Not adopted, people still using other tools
- **High search failure rate**: >30% searches with 0 results → Coverage gaps or poor search
- **Low engagement**: <10 article views/day across team → Not habit-forming, not finding value
- **High staleness**: >50% articles outdated → Not maintained, better to shut down than mislead

## Implementation Notes

### Phase 1: MVP (Target: 6 weeks)

- Web app: Create, edit, publish, search (full-text only)
- PostgreSQL database with articles, users, tags
- Basic auth (Okta SSO)
- Category browsing
- Article history (versions)

### Phase 2: AI Features (Target: +2 weeks after MVP)

- Claude API integration for tag suggestions
- Semantic search with embeddings (Pinecone)
- Related articles recommendations

### Phase 3: Slack Integration (Target: +2 weeks)

- Slack bot for search
- Notifications for watched categories
- Quick capture via /knowledge add

### Phase 4: Enhancements (Target: +4 weeks)

- Stale content detector
- Weekly digest emails
- Article analytics (views, searches that led to article)
- Improved markdown editor with live preview

### Dependencies

- Okta SSO configured with company
- Supabase account and PostgreSQL database provisioned
- Pinecone account for vector database
- Anthropic API key for Claude
- Slack workspace with bot permissions
- AWS S3 bucket for attachments

## Open Questions

- Should we allow anonymous reading (no auth) for Public articles? → Decision: No, require auth to prevent leaking company info.
- Do we need approval workflow for published articles? → Decision: No for v1. Trust engineers. Add if needed later.

## Interview Context

This specification was developed through a structured interview on 2026-01-13.

Key decisions made during interview:
- Chose semantic search over just full-text because engineering articles use varied terminology (embeddings help)
- Decided on Slack bot integration as high priority (team lives in Slack)
- Opted for version history over real-time collaborative editing (simpler, matches workflow)
- Selected Claude for tag suggestions based on quality, OpenAI for embeddings based on cost
