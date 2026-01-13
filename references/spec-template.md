# [System Name] - Work System Specification

<!--
This template provides a comprehensive structure for work system specifications.
Each section includes guidance on what to include. Remove guidance text in final spec.
-->

## Overview

- **Purpose**: [One-line summary of what this system does and why it exists]
- **Last Updated**: [Date of last modification]
- **Status**: [Draft | In Progress | Ready for Implementation | In Production]

<!--
Guidance: Keep purpose concise but specific. "Manages customer support tickets"
not "Helps with work." Status tracks maturity of the spec and system.
-->

---

## System Scope

### In Scope

[Bulleted list of what this system DOES handle]

<!--
Guidance: Be specific. Good: "Tracks bug reports from customers via email"
Bad: "Handles bugs." Include:
- Types of work/tasks this manages
- User groups supported
- Key features/capabilities
- Integrations included
-->

Examples:
- Captures customer support requests from email and web form
- Automatically categorizes requests by product area and urgency
- Routes requests to appropriate team members
- Provides dashboard for tracking resolution status

### Explicitly Out of Scope (Non-Goals)

[Bulleted list of what this system DOES NOT handle]

<!--
Guidance: Just as important as in-scope. Prevents scope creep. Include:
- Related problems you're NOT solving
- Features deliberately excluded
- Systems you're NOT replacing
- Use cases you're NOT supporting
-->

Examples:
- NOT handling billing or payment issues (use existing Stripe dashboard)
- NOT replacing Jira for internal engineering tasks
- NOT providing customer-facing status pages (use StatusPage for that)
- NOT supporting phone/voice support routing

---

## User Profiles

### Primary Users

[Describe who uses this system, their roles, typical tasks]

<!--
Guidance: Include:
- User types/roles (admin, team member, end user, etc.)
- How they interact with the system
- Their goals when using the system
- Frequency of use
-->

Example:
- **Support Team Members** (5-10 people): View assigned requests, update status, respond to customers. Daily active users.
- **Support Manager** (1 person): Monitor team performance, reassign requests, review metrics. Several times per week.
- **Customers** (100s): Submit requests via email or web form. Occasional use when they need help.

### Technical Level

[Beginner | Intermediate | Advanced] - [Description of technical sophistication]

<!--
Guidance: Important for UI/UX decisions. Include:
- Comfort with technical tools (CLI, APIs, config files)
- Need for documentation/training
- Preference for GUI vs. command-line
-->

Example: **Intermediate** - Support team comfortable with web dashboards and keyboard shortcuts, but not developers. Prefer GUI over CLI. Manager has basic SQL knowledge for custom reports.

---

## Work Flow

### Input & Capture

#### Entry Points

[How work enters the system]

<!--
Guidance: List all ways work can be submitted. For each, note:
- Source (email, form, API, etc.)
- Authentication requirements
- Validation performed
-->

Examples:
- **Email**: support@company.com (parsed automatically, creates request from sender info)
- **Web Form**: Public form at company.com/support (CAPTCHA required, validates required fields)
- **API**: POST /api/requests (requires API key, used by partners)

#### Required Metadata

[Fields captured for each work item]

<!--
Guidance: Distinguish required vs. optional fields. Include:
- Field name
- Type (text, dropdown, date, etc.)
- Source (user-provided, auto-detected, system-generated)
- Validation rules
-->

Examples:
- **Title** (required, text, user-provided): Brief description of issue
- **Description** (required, long text, user-provided): Detailed explanation
- **Product Area** (required, dropdown, auto-detected from email or user-selected): Which product this affects
- **Priority** (optional, P0-P3, auto-calculated): Urgency level based on keywords and customer tier
- **Requester** (required, email, system-captured): Who submitted this
- **Submitted At** (required, timestamp, system-generated): When received

#### Work Types

[Categories or types of work this system handles]

<!--
Guidance: If all work is treated the same, say "Single type: [name]"
If different types have different workflows, list each with:
- Type name
- How it's identified
- What makes it different from other types
-->

Examples:
- **Bug Report**: Identified by keywords ("crash", "error", "broken"). Routed to engineering team for triage.
- **Feature Request**: Identified by keywords ("wish", "would be nice", "suggestion"). Collected for quarterly review.
- **How-To Question**: Identified by question marks and lack of error terms. Answered by support team from docs.
- **Account Issue**: Identified by mention of "login", "password", "account". Requires identity verification before processing.

### Processing & Organization

#### Categorization Logic

[How work is organized into categories]

<!--
Guidance: Describe the system for organizing work. Include:
- Manual vs. automatic categorization
- Category hierarchy (flat, nested, multi-dimensional)
- Who can change categories
- How categories are used (filtering, routing, reporting)
-->

Example:
- **Automatic**: AI scans title+description, suggests product area with confidence score
- **Human review**: Support team member confirms or corrects category within 1 hour
- **Categories**: Two-level hierarchy (Product Area > Sub-Feature). E.g., "Mobile App > Push Notifications"
- **Recategorization**: Any team member can change, tracked in audit log

#### Priority Framework

[How work is prioritized]

<!--
Guidance: Explain how priority is determined and used. Include:
- Priority levels and definitions
- How priority is assigned (manual, automatic, hybrid)
- What priority affects (response SLA, routing, visibility)
- Can priority change? If so, when/why?
-->

Example:
- **P0 (Critical)**: System down, blocking all users. Auto-assigned if keywords present. Response SLA: 1 hour.
- **P1 (High)**: Major feature broken for many users. Auto-assigned or manager-set. SLA: 4 hours.
- **P2 (Normal)**: Standard issue affecting small number of users. Default. SLA: 24 hours.
- **P3 (Low)**: Minor issue or feature request. Auto-assigned for non-urgent keywords. SLA: 5 business days.
- **Escalation**: P2 auto-escalates to P1 if unresponded after 36 hours.

#### Workflow States

[States work items progress through]

<!--
Guidance: Define the lifecycle. For each state, include:
- State name and description
- What triggers transition to this state
- Who can perform the transition
- What happens in this state
-->

Example:
1. **New**: Just submitted, not yet reviewed (auto-assigned on intake)
2. **Triaged**: Reviewed, categorized, priority set (by team member within 1 hour of submission)
3. **Assigned**: Routed to specific team member (automatically by product area, or manually by manager)
4. **In Progress**: Team member actively working on it (set when team member adds comment or starts investigation)
5. **Waiting on Customer**: Need more info from requester (team member sends question, auto-sets this state)
6. **Resolved**: Solution provided (team member marks resolved with resolution note)
7. **Closed**: Customer confirmed or 7 days passed (auto-closes if no customer response, or customer clicks "solved" link)

#### Automation Rules

[Automated actions the system performs]

<!--
Guidance: List each automation with trigger and action. Include:
- What triggers the automation
- What action is taken
- Any conditions or thresholds
- Failure handling
-->

Examples:
- **Auto-categorize**: On submission, AI suggests product area (if confidence > 80%, apply automatically; else flag for review)
- **Auto-assign**: When state = Triaged, route to team member based on: product area specialty, current workload, availability status
- **Auto-escalate**: If state = Assigned for > 36 hours without response, change priority P2→P1 and notify manager
- **Auto-close**: If state = Resolved for 7 days without customer response, set to Closed
- **Auto-notify customer**: On state change to Resolved, send email with solution and "Was this helpful?" link

### Output & Interaction

#### User Interface

[How users interact with the system]

<!--
Guidance: Describe the interface(s). Include:
- Type (web, CLI, mobile, chat bot, API, etc.)
- Key views or screens
- Navigation patterns
- Accessibility considerations
-->

Example:
- **Primary**: Web dashboard at support.internal.company.com
  - **Queue View**: List of assigned requests, sortable by priority/age, with quick status change buttons
  - **Detail View**: Full request with history, comments, attachments, and action buttons
  - **Metrics View**: Charts showing volume, response time, resolution rate (manager-only)
- **Secondary**: Email notifications with direct links to detail view
- **Future**: Slack bot for quick status checks (not v1)

#### Key Actions

[What users can do with work items]

<!--
Guidance: List primary actions. For each, include:
- Action name
- Who can perform it
- Where in UI
- What it does
-->

Examples:
- **View Details**: All users, click on request in queue view, shows full history and metadata
- **Add Comment**: Assigned team member, detail view, adds timestamped note (visible to team and customer)
- **Change Status**: Assigned team member or manager, detail view, transitions state (see Workflow States)
- **Reassign**: Manager only, detail view, changes assignee and notifies new owner
- **Change Priority**: Manager or auto-escalation, detail view, updates priority level
- **Attach File**: Team member, detail view, uploads screenshot or document related to request
- **Link Related**: Team member, detail view, creates connection to duplicate or related requests

#### Notifications/Alerts

[When and how users are notified]

<!--
Guidance: For each notification type, include:
- What triggers it
- Who receives it
- Channel (email, Slack, in-app, etc.)
- Frequency (immediate, digest, etc.)
- User configurability
-->

Examples:
- **New Assignment**: When request assigned to you, immediate email with request details and link
- **Status Change**: When your submitted request changes state, immediate email to customer
- **SLA Warning**: When your assigned request approaching SLA deadline, in-app notification + email 1 hour before
- **Daily Digest**: All open requests assigned to you, email sent at 8am every weekday (user can disable)
- **Escalation**: When request auto-escalates, immediate Slack message to manager

---

## Technical Architecture

### Technology Stack

<!--
Guidance: List technologies for each layer. Include version constraints if relevant.
Be specific about frameworks, libraries, and tools.
-->

- **Frontend**: [Framework/language]
- **Backend**: [Framework/language]
- **Database**: [Type and specific product]
- **Hosting**: [Where deployed]
- **Integrations**: [External services]

Example:
- **Frontend**: React 18 with TypeScript, Tailwind CSS, deployed to Vercel
- **Backend**: Node.js 20 with Express, TypeScript
- **Database**: PostgreSQL 15 hosted on Supabase (includes row-level security and real-time subscriptions)
- **Email**: SendGrid API for outbound, AWS SES + custom parser for inbound
- **AI**: Claude API (Anthropic) for categorization and summarization
- **Hosting**: Backend on Railway, database on Supabase, frontend on Vercel
- **Monitoring**: Sentry for errors, PostHog for analytics

### Data Model

[Key entities and relationships]

<!--
Guidance: Describe main data entities. For each, include:
- Entity name
- Key fields
- Relationships to other entities
- Unique constraints or indexes

Can use ERD diagram, tables, or prose. Keep concise.
-->

Example:

**Request**
- id, title, description, product_area, priority, status, requester_email, assignee_id, created_at, updated_at
- Has many Comments
- Belongs to one User (assignee)

**Comment**
- id, request_id, author_id, body, created_at, is_internal (visible to team only)
- Belongs to one Request
- Belongs to one User (author)

**User**
- id, email, name, role (team_member | manager), status (active | away), product_areas (array)
- Has many assigned Requests
- Has many authored Comments

### AI/Automation Components

[What AI capabilities are used and how]

<!--
Guidance: For each AI/automation feature, describe:
- What it does
- Which AI service/model
- Input and output
- Accuracy requirements
- Fallback if AI fails or uncertain
- Cost implications
-->

Examples:

**Auto-categorization**
- **Purpose**: Suggest product area from title+description
- **Model**: Claude 3.5 Sonnet via Anthropic API
- **Input**: Request title and description
- **Output**: Product area + confidence score (0-100%)
- **Threshold**: Auto-apply if confidence > 80%, else flag for human review
- **Fallback**: If API fails, mark as "Uncategorized" and notify team
- **Cost**: ~$0.01 per request (acceptable)

**Smart Routing**
- **Purpose**: Assign to best team member based on expertise and workload
- **Logic**: Rule-based algorithm (not LLM)
  - Filter team members by product area specialty
  - Among specialists, assign to one with fewest open P0/P1 requests
  - If all specialists busy, round-robin among all team members
- **Fallback**: If no team members available (all away status), assign to manager

---

## Edge Cases & Error Handling

<!--
Guidance: List scenarios that could go wrong and how to handle them.
Think about: invalid input, external service failures, high load, data conflicts, etc.
-->

**Scenario 1: Email parsing fails (malformed email, no text content)**
- **Handling**: Create request with title "Email Parsing Error", attach raw email, assign to manager for manual processing

**Scenario 2: AI categorization API timeout or error**
- **Handling**: Retry once after 2 seconds. If still fails, mark as "Uncategorized" and log error to Sentry. Team member will categorize manually.

**Scenario 3: Duplicate request submitted (same requester, same issue within 24 hours)**
- **Handling**: AI detects likely duplicate (similarity score > 90%). Create request but mark as "Possible Duplicate" with link to original. Team member decides whether to merge or keep separate.

**Scenario 4: Customer replies to resolved request**
- **Handling**: Detect reply to closed request. Reopen request (change state from Closed → In Progress) and notify original assignee.

**Scenario 5: SLA breach (request not responded to within SLA time)**
- **Handling**: Log SLA breach event, escalate priority by one level, notify manager with details. No auto-closing or other destructive action.

**Scenario 6: Assignee goes on vacation (status = away) with open requests**
- **Handling**: When user sets status to away, show prompt to reassign open requests. If not reassigned, manager gets notification with list of requests needing reassignment.

---

## Security & Privacy Considerations

<!--
Guidance: Address data sensitivity, access control, compliance. Include:
- What sensitive data exists
- Who can access what
- How data is protected (encryption, access logs, etc.)
- Compliance requirements
- Data retention and deletion policies
-->

**Data Sensitivity**
- Customer emails and names (PII)
- Request descriptions may contain sensitive information (bugs might expose security issues)
- Internal comments should never be visible to customers

**Access Control**
- **Team Members**: Can view all requests, edit assigned requests, comment on any
- **Managers**: All team member permissions + reassign any request + view all metrics
- **Customers**: Can only view their own requests via unique token link in email (no login required)

**Data Protection**
- All data encrypted at rest (PostgreSQL native encryption)
- All connections use TLS 1.3
- API keys stored in environment variables, never in code
- Request attachments scanned for malware before storage

**Compliance**
- **GDPR**: Customers can request deletion via privacy@company.com (manual process, delete all requests and comments from that email)
- **Data Retention**: Closed requests retained for 2 years, then archived to cold storage. Deleted after 7 years.

**Audit Trail**
- All status changes, reassignments, and priority changes logged with timestamp and actor
- Logs retained for 1 year for debugging and compliance

---

## Success Metrics

### Primary Metric

[The main measure of success for this system]

<!--
Guidance: Should be specific, measurable, and tied to the core goal.
Include current baseline if known, and target.
-->

Example: **Average time to first response**
- **Current** (without system): ~8 hours
- **Target**: < 2 hours for P0/P1, < 24 hours for P2/P3
- **Measurement**: Timestamp of first team member comment minus submitted timestamp

### Secondary Metrics

[Supporting measures]

<!--
Guidance: 2-5 additional metrics that indicate health and value
-->

Examples:
- **Customer satisfaction**: % of "Was this helpful? Yes" clicks. Target: > 80%
- **Request volume handled**: Requests closed per week. Baseline: 150, Target: 200+ (demonstrating improved efficiency)
- **SLA compliance**: % of requests responded within SLA. Target: > 95%
- **Auto-categorization accuracy**: % of AI categories accepted without change. Target: > 80%

### Failure Indicators

[Signals that the system isn't working]

<!--
Guidance: What would make you abandon this approach?
-->

Examples:
- Average time to first response INCREASES (system adds overhead instead of reducing it)
- Team members bypass system and handle requests via direct email (system not adopted)
- > 50% of requests require manual recategorization (AI not helpful)
- Customer satisfaction falls below 70% (system degrading experience)

---

## Implementation Notes

### Phase 1: MVP (Target: 4 weeks)

<!--
Guidance: What's the minimal viable version? What's necessary for basic functionality?
-->

Examples:
- Email inbound parsing and request creation
- Web dashboard with queue view and detail view
- Manual categorization and assignment
- Basic status workflow (New → Assigned → Resolved → Closed)
- Email notifications on assignment and resolution

### Phase 2: Enhancements (Target: +2 weeks after MVP)

<!--
Guidance: What comes next after MVP is proven?
-->

Examples:
- AI auto-categorization
- Smart routing based on product area and workload
- SLA tracking and auto-escalation
- Metrics dashboard for manager
- Web form for customer submission

### Phase 3: Future (No timeline)

<!--
Guidance: What's on the wishlist but not committed?
-->

Examples:
- Slack bot integration for quick status checks
- Mobile app for team members
- Customer self-service portal (view all their historical requests)
- Integration with Jira (link support requests to engineering tickets)

### Dependencies

<!--
Guidance: What must exist or be set up before implementation can start?
-->

Examples:
- Anthropic API key for Claude access
- SendGrid account for outbound email
- AWS SES set up and verified for inbound email parsing
- Supabase account and project created
- support@company.com email address configured to forward to AWS SES

---

## Open Questions

<!--
Guidance: List any unresolved decisions or areas needing more research.
Remove this section once all questions are answered.
-->

Examples:
- Should we support attachments from email? If so, what's the size limit?
- Do we need to track time spent on each request? (Not in MVP, decide for Phase 2)
- Should customers be able to see status updates in real-time, or just email notifications?

---

## Interview Context

<!--
Guidance: Link or reference to the conversation where this spec was developed.
Helps with future questions about intent or decisions.
-->

This specification was developed through a structured interview on [Date] with [Person/Team].
Conversation transcript: [Link to Claude conversation or Google Doc or meeting notes]

Key decisions made during interview:
- Decided to use AI for categorization after discussing accuracy vs. manual effort tradeoff
- Chose Supabase over self-hosted PostgreSQL to reduce ops overhead
- Prioritized email over Slack integration based on where support requests currently come from
