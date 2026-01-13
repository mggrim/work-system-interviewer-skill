# Question Framework for Work System Interviews

## Introduction

This document provides a comprehensive catalog of interview questions organized by category. Use these questions to conduct thorough interviews that capture all aspects of a work system specification.

**Purpose of structured questions:**
- Ensure comprehensive coverage (nothing forgotten)
- Guide users who don't know what to specify
- Prevent common oversights (edge cases, non-goals, success metrics)
- Create better specs through active prompting

**How to use this framework:**
- Start with core questions from each category
- Adapt follow-ups based on complexity signals in answers
- Don't ask all questions—select based on system needs
- Ask 3-4 questions at a time (don't overwhelm)
- Drill deeper when answers reveal complexity

---

## Category 1: System Purpose & Scope

### Core Questions (Always Ask)

**Q1.1: What types of work/tasks will this system handle?**
- Ask for: Specific examples, not abstract categories
- Follow-up if vague: "Can you give 3-5 concrete examples?"
- Drill deeper if: Multiple work types mentioned → Ask about differences between them

**Q1.2: What are the explicit non-goals? (What should this NOT do?)**
- Why important: Prevents scope creep and sets boundaries
- Follow-up: "What related problems are you NOT trying to solve?"
- Common answers: "Not building X", "Not replacing Y", "Not supporting Z use case"

**Q1.3: Who are the primary users?**
- Ask for: User types/roles, technical sophistication, frequency of use
- Follow-up if multiple users: "Do different users have different needs or permissions?"
- Drill deeper if: Non-technical users → Ask about training, UI simplicity

### Additional Questions (Ask if Relevant)

**Q1.4: What's the core problem you're solving?**
- Use when: User hasn't articulated the "why"
- Follow-up: "What pain point does this eliminate?"

**Q1.5: What's in scope for v1 vs. later phases?**
- Use when: System seems large or complex
- Follow-up: "What's the minimum viable version?"

**Q1.6: Are there existing solutions you've tried?**
- Use when: Common problem domain (task management, etc.)
- Follow-up: "What didn't work about them?"

**Q1.7: What makes this system unique to your needs?**
- Use when: Generic requirements that could use off-the-shelf
- Follow-up: "Why build custom vs. use existing tool?"

### Adaptive Follow-ups

**If user mentions:**
- "Multiple departments" → Ask about different workflows per department
- "Compliance" → Ask about specific regulations (HIPAA, GDPR, SOC2)
- "Replace existing system" → Ask about migration, data import, training
- "AI/automation" → Ask what should be automated vs. manual

---

## Category 2: Input & Triggers

### Core Questions (Always Ask)

**Q2.1: How does work enter the system?**
- Common options: Email, Slack, web form, manual entry, API, webhooks, file upload
- Follow-up: "Are there multiple entry points?" → If yes, ask if they're treated differently
- Drill deeper if: Integration mentioned → Ask about authentication, API access

**Q2.2: What metadata needs to be captured at intake?**
- Common fields: Title, description, priority, category, requester, deadline, attachments
- Follow-up: "Which fields are required vs. optional?"
- Drill deeper if: Complex categorization → Ask about taxonomy, auto-tagging

**Q2.3: Are there different work types requiring different processing?**
- Examples: Bug vs. feature, urgent vs. routine, internal vs. external
- Follow-up if yes: "How many types? What makes them different?"
- Drill deeper if: Many types → Ask about type detection (manual, rules, AI)

### Additional Questions (Ask if Relevant)

**Q2.4: Should intake be validated or gated?**
- Use when: Quality concerns or spam potential
- Examples: Required fields, approval workflow, duplicate detection
- Follow-up: "What happens to invalid submissions?"

**Q2.5: How is priority/urgency determined?**
- Use when: Not addressed in Q2.2
- Options: User-set, automatic rules, AI assessment, SLA-based
- Follow-up: "Can priority change after intake?"

**Q2.6: Who can submit work to the system?**
- Use when: Security or access control matters
- Follow-up: "Authentication required? Public submissions allowed?"

**Q2.7: Should there be intake notifications?**
- Use when: Multi-user or team system
- Follow-up: "Who gets notified? What triggers notification?"

**Q2.8: How should batch submissions be handled?**
- Use when: High volume or bulk import scenarios
- Examples: CSV upload, API batch, scheduled pulls

### Adaptive Follow-ups

**If user mentions:**
- "Email" → Ask about: parsing rules, attachments, threading, spam filtering
- "Slack" → Ask about: which channels, slash commands, reactions as actions
- "API" → Ask about: authentication, rate limits, webhook vs. polling
- "Form" → Ask about: public vs. authenticated, validation, CAPTCHA
- "File upload" → Ask about: formats, parsing, size limits, storage

---

## Category 3: Processing & Organization

### Core Questions (Always Ask)

**Q3.1: How should work be categorized?**
- Options: Manual tags, automatic rules, AI classification, folder hierarchy
- Follow-up: "Who decides the categories?" (User, system, predefined list)
- Drill deeper if: AI classification → Ask about training data, accuracy needs

**Q3.2: How should work be prioritized?**
- Options: Manual ranking, scoring system, SLA-based, AI recommendation
- Follow-up: "Can priority change over time?" (e.g., age-based escalation)
- Drill deeper if: Complex priority → Ask about framework (P0-P3, MoSCoW, etc.)

**Q3.3: What workflows or states does work move through?**
- Minimum: New → In Progress → Done
- Complex: New → Triaged → Assigned → In Progress → Review → Done → Archived
- Follow-up: "What triggers state transitions?" (Manual, automatic, time-based)

### Additional Questions (Ask if Relevant)

**Q3.4: What automation or AI assistance should be applied?**
- Examples: Auto-categorization, smart routing, summarization, duplicate detection
- Follow-up: "What should remain manual?" (Important for setting scope)

**Q3.5: Should work items be assigned to people/teams?**
- Use when: Multi-user system
- Follow-up: "How does assignment work?" (Manual, round-robin, skill-based, AI)

**Q3.6: Are there dependencies between work items?**
- Use when: Complex project management needs
- Follow-up: "How are dependencies tracked? Blockers handled?"

**Q3.7: Should there be time tracking or SLAs?**
- Use when: Accountability or compliance matters
- Follow-up: "What happens when SLA is breached?"

**Q3.8: How should duplicates be handled?**
- Use when: Multiple entry points or high volume
- Options: Prevent, flag for review, auto-merge, link related

**Q3.9: Are there recurring or templated work items?**
- Use when: Repetitive work patterns
- Examples: Weekly reports, monthly reviews, seasonal campaigns

**Q3.10: Should work be grouped or linked?**
- Use when: Related work items (projects, epics, campaigns)
- Follow-up: "Hierarchy or flat with links?"

### Adaptive Follow-ups

**If user mentions:**
- "AI" → Ask about: what AI should do, confidence thresholds, human review
- "Teams" → Ask about: workload balancing, skill matching, availability
- "Rules" → Ask about: rule complexity, maintenance, conflict resolution
- "Automation" → Ask about: error handling, rollback, audit trail

---

## Category 4: Output & Action

### Core Questions (Always Ask)

**Q4.1: How do users interact with organized work?**
- Options: Web dashboard, CLI, mobile app, chat bot, email digest, API
- Follow-up: "Single interface or multiple?" → If multiple, which is primary?
- Drill deeper if: Web dashboard → Ask about views (list, board, calendar, timeline)

**Q4.2: What actions can be taken on work items?**
- Common: View, edit, assign, prioritize, comment, attach files, link, archive, delete
- Follow-up: "Do different users have different permissions?"
- Drill deeper if: Workflows → Ask about state transitions, approval gates

### Additional Questions (Ask if Relevant)

**Q4.3: What views or filters should be available?**
- Examples: By priority, by assignee, by date, by category, custom filters
- Follow-up: "Saved views? Default views per user?"

**Q4.4: Should there be notifications or alerts?**
- Use when: Multi-user or time-sensitive
- Ask about: What triggers notification, channels (email, Slack, push), frequency
- Follow-up: "User-configurable? Quiet hours?"

**Q4.5: Are reports or analytics needed?**
- Use when: Management oversight or optimization
- Examples: Volume trends, cycle time, bottlenecks, team velocity
- Follow-up: "Who views reports? How often?"

**Q4.6: Should there be search capabilities?**
- Use when: Large volume expected
- Ask about: Full-text, metadata filters, advanced queries, saved searches

**Q4.7: Is collaboration needed on work items?**
- Use when: Multi-user system
- Examples: Comments, @mentions, file sharing, real-time editing

**Q4.8: Should there be an audit trail?**
- Use when: Compliance or debugging needs
- Ask about: What's logged, retention period, who can access

### Adaptive Follow-ups

**If user mentions:**
- "Dashboard" → Ask about: real-time updates, customization, role-based views
- "CLI" → Ask about: scripting, automation, JSON output, interactive vs. command
- "Mobile" → Ask about: offline support, push notifications, feature parity
- "Notifications" → Ask about: noise concerns, digest options, escalation rules

---

## Category 5: Technical Implementation

### Core Questions (Always Ask)

**Q5.1: What technologies/platforms are you comfortable with?**
- Languages: JavaScript/Node, Python, Go, Rust, Java, etc.
- Follow-up: "Do you have preferences or constraints?"
- Drill deeper if: "Whatever works" → Recommend based on requirements

**Q5.2: Are there existing tools to integrate with?**
- Common: Slack, email, GitHub, Jira, Linear, Notion, Google Workspace
- Follow-up for each: "Read-only or read/write? API access available?"
- Drill deeper if: Many integrations → Ask about orchestration, data sync

**Q5.3: What are your performance/scale requirements?**
- Ask about: Items per day, concurrent users, response time needs, storage growth
- Follow-up: "Current volume? Expected growth?"
- Drill deeper if: High scale → Ask about caching, async processing, sharding

### Additional Questions (Ask if Relevant)

**Q5.4: Where should this be deployed?**
- Options: Local machine, team server, cloud (AWS/GCP/Azure), serverless
- Follow-up: "Who maintains it? What's your ops experience?"

**Q5.5: What's your database preference?**
- Options: SQLite (simple, local), Postgres (robust), MongoDB (flexible), files (simplest)
- Provide recommendation based on: Scale, queries, relationships, ops overhead

**Q5.6: Should this have an API?**
- Use when: Integrations or programmatic access needed
- Follow-up: "REST, GraphQL, or RPC? Authentication?"

**Q5.7: Are there cost constraints?**
- Use when: Cloud services or paid APIs mentioned
- Follow-up: "Budget ceiling? Prefer self-hosted to minimize costs?"

**Q5.8: What about AI/LLM usage?**
- Options: Claude API, OpenAI API, local models (Ollama), no AI initially
- Follow-up: "Cost tolerance for API calls? Latency sensitivity?"

**Q5.9: Should the system support multiple environments?**
- Use when: Team use or staged rollout
- Examples: Dev, staging, production with different configs

**Q5.10: What's the disaster recovery plan?**
- Use when: Critical data
- Ask about: Backups, restoration, redundancy

### Adaptive Follow-ups

**If user mentions:**
- "Slack" → Ask about: bot user vs. app, slash commands, interactive components
- "Cloud" → Ask about: Provider preference, region, cost monitoring
- "AI" → Ask about: Use cases, fallback if AI fails, cost vs. accuracy tradeoffs
- "High volume" → Ask about: Queueing, rate limiting, horizontal scaling

---

## Category 6: Edge Cases & Concerns

### Core Questions (Always Ask)

**Q6.1: What failure modes worry you most?**
- Common concerns: Data loss, missed items, incorrect categorization, system downtime
- Follow-up: "Which would be catastrophic vs. merely annoying?"
- Drill deeper if: Data loss concern → Ask about backups, validation

**Q6.2: How should the system handle ambiguity or incomplete information?**
- Scenarios: Missing required fields, unclear category, conflicting data
- Options: Block submission, flag for review, make best guess, ask for clarification
- Follow-up: "Who resolves ambiguity? Human review or AI decision?"

### Additional Questions (Ask if Relevant)

**Q6.3: What privacy/security concerns exist?**
- Ask about: Sensitive data (PII, credentials), access control, encryption
- Follow-up: "Compliance requirements (GDPR, HIPAA, SOC2)?"

**Q6.4: What happens when integrations fail?**
- Use when: External dependencies mentioned
- Ask about: Retry logic, fallback behavior, notification of failures

**Q6.5: How should the system handle high load or rate limits?**
- Use when: Variable volume expected
- Options: Queue, throttle, reject, backpressure

**Q6.6: What about data quality and validation?**
- Use when: User input or automated ingestion
- Ask about: Required fields, format validation, sanity checks

**Q6.7: Should there be safeguards against accidental actions?**
- Examples: Confirmation for delete, undo/redo, soft delete with recovery
- Use when: Destructive operations possible

**Q6.8: What if the system receives malicious input?**
- Use when: Public-facing or external submissions
- Ask about: Sanitization, rate limiting, CAPTCHA, moderation

### Adaptive Follow-ups

**If user mentions:**
- "Customer data" → Ask about: encryption at rest, access logs, GDPR compliance
- "External API" → Ask about: timeout handling, retry strategy, circuit breaker
- "High stakes" → Ask about: approval workflows, audit trails, rollback capability

---

## Category 7: Success Metrics

### Core Questions (Always Ask)

**Q7.1: How will you know if this system is working well?**
- Push for: Specific, measurable metrics (not "it works")
- Examples: Time saved, items processed, error rate, user satisfaction
- Follow-up: "What's the target or goal for this metric?"

**Q7.2: What would make you abandon this approach?**
- Why important: Defines failure conditions and helps avoid them
- Common answers: Too manual, doesn't scale, hard to maintain, users won't adopt
- Follow-up: "What would you try instead?"

### Additional Questions (Ask if Relevant)

**Q7.3: What's the main metric that matters most?**
- Use when: Multiple metrics mentioned in Q7.1
- Purpose: Prioritize implementation efforts

**Q7.4: Are there leading indicators of success/failure?**
- Examples: Early adoption rate, submission volume, processing speed
- Use when: Long-term metrics hard to measure initially

**Q7.5: How will you collect these metrics?**
- Use when: Analytics not yet considered
- Ask about: Built-in dashboards, external analytics, manual tracking

**Q7.6: What's the ROI or value proposition?**
- Use when: Significant build effort
- Ask about: Time saved, cost reduced, revenue enabled

### Adaptive Follow-ups

**If user mentions:**
- "Time saved" → Ask about: Current time spent, target reduction, measurement method
- "User satisfaction" → Ask about: Survey method, frequency, target score
- "Volume" → Ask about: Baseline, growth target, capacity planning

---

## Adaptive Follow-up Patterns

### When to Drill Deeper

**Complexity signals that warrant more questions:**

1. **"Multiple"** (user types, workflows, integrations, data sources)
   - Ask about each one specifically
   - Ask how they differ or interact
   - Ask about priorities if can't support all initially

2. **"Integration"** (with external tool/service)
   - Ask about API access, authentication, rate limits
   - Ask about sync frequency and direction (read, write, both)
   - Ask about failure handling

3. **"AI" or "automatic"**
   - Ask what should be automated vs. manual
   - Ask about accuracy needs, confidence thresholds
   - Ask about fallback when AI is uncertain

4. **"Scale" or "volume"**
   - Get specific numbers (items/day, users, data size)
   - Ask about growth expectations
   - Ask about performance requirements

5. **"Team" or "collaboration"**
   - Ask about roles and permissions
   - Ask about concurrent editing, conflicts
   - Ask about communication needs

6. **"Compliance" or "security"**
   - Ask about specific regulations
   - Ask about audit requirements
   - Ask about data retention, deletion

### When to Provide Options

**Offer choices when user may not know all options:**

- **Storage:** "SQLite is simplest for local, Postgres if you need robustness, files if you want maximum simplicity"
- **Interface:** "CLI if you're technical, web dashboard if multiple users, bot if conversational"
- **Hosting:** "Local if just you, cloud if team access, self-hosted server if you have ops skills"
- **AI provider:** "Claude API for high quality, OpenAI for ecosystem, local models for privacy/cost"

### When to Challenge Assumptions

**Politely question if:**
- Scope seems too broad → "Could we start with a subset for v1?"
- Tech choice seems mismatched → "Given your requirements, have you considered X instead?"
- Success metric seems vague → "How would you measure that specifically?"
- Edge case seems unaddressed → "What happens if X fails?"

---

## Question Delivery Best Practices

### Batch Size
- Ask 3-4 questions at a time (not overwhelming)
- Wait for answers before asking more
- Adapt next batch based on previous answers

### Question Format
Use AskUserQuestion tool for structured questions, or free-form for follow-ups:

**Structured (use tool):**
```
Category: [Name]

1. [Question with context]
2. [Question with context]
3. [Question with context]

Feel free to answer in shorthand or full detail—whatever works best.
```

**Free-form follow-up:**
```
You mentioned [X]. Can you elaborate on [specific aspect]?
```

### Tone
- Conversational, not interrogative
- Explain why you're asking when not obvious
- Acknowledge good answers ("That's helpful context")
- Offer examples when user seems stuck

### Flexibility
- Don't ask irrelevant questions (e.g., team questions for single-user systems)
- Skip categories if already answered elsewhere
- Combine related questions if topics overlap
- Stop early if system is simple (don't force 15 questions)

### Summarize Periodically
Every 5-6 questions, provide brief summary:
```
So far I understand:
- [Key point 1]
- [Key point 2]
- [Key point 3]

Now let's discuss [next category]...
```

---

## Interview Checklist

Before moving to spec generation, ensure you've covered:

- ☐ **Purpose:** What problem this solves
- ☐ **Scope:** What's in/out, non-goals
- ☐ **Users:** Who uses it, technical level
- ☐ **Input:** How work enters, metadata captured
- ☐ **Processing:** Categorization, prioritization, workflow states
- ☐ **Output:** Interface, actions users can take
- ☐ **Technical:** Stack, integrations, scale requirements
- ☐ **Edge cases:** Failure modes, ambiguity handling
- ☐ **Security:** Privacy, access control (if applicable)
- ☐ **Success:** Metrics, failure conditions

If any area feels shallow, ask 1-2 more targeted questions before generating spec.
