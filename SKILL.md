---
name: work-system-interviewer
description: Helps users design and specify AI-based systems for organizing and executing incoming work through comprehensive structured interviews. Use this skill when users want to create, refine, or document systems for task management, project organization, knowledge management, automation workflows, or communication/collaboration. Triggers include requests to "design a work system", "create a task management approach", "build an automation workflow", "organize my work", "manage incoming requests", or when iteratively refining existing work system specifications. This skill conducts thorough interviews (8-15+ questions) covering technical implementation, UI/UX, edge cases, success metrics, and non-goals, then generates structured markdown specifications ready for implementation.
license: Complete terms in LICENSE.txt
---

# Work System Interviewer

## Overview

This skill guides you through comprehensive structured interviews to design AI-based systems for organizing and executing incoming work. Whether you're building task management, knowledge management, automation workflows, or communication/collaboration systems, this skill ensures nothing important is forgotten through systematic questioning.

**What you get:**
- Thorough interview covering all aspects (8-15+ questions)
- Structured markdown specification ready for implementation
- Support for iterative refinement as your system evolves
- Clear handoff to implementation with full context

**When to use:**
- Creating new work organization systems
- Refining existing system specifications
- Documenting work system requirements
- Planning automation workflows

---

# 🚀 High-Level Workflow

Creating a comprehensive work system specification involves five phases:

## Phase 1: Initial Context Gathering (5-10 min)
- Understand your starting point (new system or refinement)
- Capture high-level vision
- Determine spec file location
- Assess system complexity

## Phase 2: Comprehensive Interview (15-30 min)
- System Purpose & Scope (what's in/out)
- Input & Triggers (how work enters)
- Processing & Organization (how work is managed)
- Output & Action (how users interact)
- Technical Implementation (technology choices)
- Edge Cases & Concerns (failure modes, constraints)
- Success Metrics (how you'll measure success)

## Phase 3: Spec Generation (5 min)
- Generate structured markdown specification
- Validate completeness with automated checks
- Write to your specified location

## Phase 4: Review & Next Steps (5 min)
- Present what was captured
- Offer implementation options
- Load spec context for next steps

## Phase 5: Iterative Refinement (optional, ongoing)
- Update existing specs with targeted questions
- Track changes between versions
- Evolve system over time

---

# Phase 1: Initial Context Gathering

## Detecting Starting Point

**New system:** If this is your first time, we'll start from scratch with a comprehensive interview.

**Existing spec:** If you have an existing spec, provide the file path. I'll read it, identify areas needing work (✓ Complete, ⚠️ Needs refinement, ❌ Missing), and we'll focus our interview on specific sections.

## High-Level Vision

Start by describing your work system in 1-3 sentences. Don't worry about details yet—just capture the essence:
- What kind of work does it handle?
- Who will use it?
- What problem does it solve?

Example: "I need a system to track incoming customer support requests, automatically categorize them, and route to the right team members. It should integrate with our email and Slack."

## Spec File Location

I'll ask where you want to save the specification. Common options:
- Project root: `./WORK_SYSTEM_SPEC.md`
- Dedicated directory: `./docs/work-system-spec.md`
- User's .claude directory: `~/.claude/work-systems/[name]-spec.md`

## Complexity Assessment

Based on your description, I'll gauge complexity to determine interview depth:
- **Simple** (8-10 questions): Single user, one workflow, local-only
- **Standard** (10-12 questions): Multiple workflows, some integrations
- **Complex** (12-15+ questions): Multiple user types, many integrations, scale concerns, compliance requirements

---

# Phase 2: Comprehensive Interview

## Introduction

I'll conduct a thorough interview with 8-15+ questions to ensure we capture everything needed for implementation. Questions are organized into categories, and I'll ask 3-4 at a time to avoid overwhelming you.

Feel free to answer in shorthand, bullet points, or dump information however works best. I'll adapt follow-up questions based on what you share.

## Core Question Categories

### Category 1: System Purpose & Scope (2-3 questions)

**Key questions:**
- What types of work/tasks will this system handle? Be specific about work types.
- What are the explicit **non-goals**? (What should this NOT do?)
- Who are the primary users and what's their technical sophistication?

**Why this matters:** Clear scope prevents creep and ensures the system stays focused. Non-goals are as important as goals.

### Category 2: Input & Triggers (2-3 questions)

**Key questions:**
- How does work enter the system? (Email, Slack, forms, manual entry, API, webhooks?)
- What metadata needs to be captured at intake? (Priority, category, requester, deadline?)
- Are there different work types requiring different processing?

**Why this matters:** The entry points determine integration complexity and data capture requirements.

### Category 3: Processing & Organization (2-3 questions)

**Key questions:**
- How should work be categorized/prioritized? (Manual, automatic, AI-assisted?)
- What workflows or states does work move through? (New → In Progress → Done? More complex?)
- What automation or AI assistance should be applied? (Auto-categorization, smart routing, summarization?)

**Why this matters:** This is the core logic of your system—how work flows and transforms.

### Category 4: Output & Action (1-2 questions)

**Key questions:**
- How do users interact with organized work? (Dashboard, CLI, notifications, API?)
- What actions can be taken on work items? (Assign, prioritize, comment, archive, defer?)

**Why this matters:** The interface determines usability and adoption.

### Category 5: Technical Implementation (2-3 questions)

**Key questions:**
- What technologies/platforms are you comfortable with? (Node/Python/Go? SQLite/Postgres? Local/cloud?)
- Are there existing tools to integrate with? (Slack, email, Jira, GitHub, linear?)
- What are your performance/scale requirements? (How many items per day? Response time needs?)

**I'll provide options** for common choices:
- Storage: Local files, SQLite, PostgreSQL, MongoDB, cloud APIs
- Interface: CLI, web app, chat bot, API
- AI/LLM: Local models, Claude API, OpenAI API
- Deployment: Local script, Docker, serverless, VPS

**Why this matters:** Technical choices constrain implementation and determine complexity.

### Category 6: Edge Cases & Concerns (1-2 questions)

**Key questions:**
- What failure modes worry you most? (Data loss, missed items, incorrect categorization?)
- How should the system handle ambiguity or incomplete information?
- What privacy/security concerns exist? (Sensitive data, access control, audit logs?)

**Why this matters:** Edge cases define system robustness. Better to think through now than discover in production.

### Category 7: Success Metrics (1-2 questions)

**Key questions:**
- How will you know if this system is working well? (Time saved? Items processed? User satisfaction?)
- What would make you abandon this approach? (Too much manual work? Doesn't scale? Hard to maintain?)

**Why this matters:** Success criteria define "done" and guide implementation priorities.

## Interview Strategy

### Adaptive Depth

I'll adapt based on your answers:
- **Simple answers** → Move to next category
- **Complex answers** → Drill deeper with 2-3 sub-questions
- **Mentions integrations** → Ask about APIs, auth, data formats
- **Mentions multiple users** → Ask about roles, permissions, workflows
- **Mentions scale** → Ask about volume, performance, bottlenecks

### Question Delivery Pattern

I'll ask questions in digestible batches using the AskUserQuestion tool:

```markdown
## [Category Name] (Question 1 of 3)

Let me understand [aspect]:

1. [Question 1]
2. [Question 2]
3. [Question 3]

Answer in shorthand or full sentences—whatever works for you.
```

### Full Question Catalog

For the complete list of questions across all categories with guidance on when to use each, see [question-framework.md](./references/question-framework.md).

---

# Phase 3: Spec Generation

## Using the Template

I'll generate a structured markdown specification using the template from [spec-template.md](./references/spec-template.md).

## Spec Structure

Your specification will include:

**Core sections:**
- Overview (purpose, status, last updated)
- System Scope (in/out of scope, explicit non-goals)
- User Profiles (who uses it, technical level)

**Work flow:**
- Input & Capture (entry points, metadata, work types)
- Processing & Organization (categorization, priority, states, automation)
- Output & Interaction (UI, actions, notifications)

**Technical details:**
- Technology Stack (frontend, backend, database, integrations)
- Data Model (key entities and relationships)
- AI/Automation Components (what's automated, how)

**Risk & success:**
- Edge Cases & Error Handling (scenarios and solutions)
- Security & Privacy Considerations (data sensitivity, access control)
- Success Metrics (primary/secondary metrics, failure indicators)

**Implementation:**
- Implementation Notes (phases, dependencies)
- Open Questions (remaining uncertainties)
- Interview Context (link to this conversation)

## Validation

After generating the spec, I'll run `scripts/validate_spec.py` to check completeness:
- ✓ **Complete sections**: All required content present
- ⚠️ **Incomplete sections**: Section exists but needs more detail
- ❌ **Missing sections**: Required section not found

If validation finds issues, I'll ask targeted follow-up questions to fill gaps.

---

# Phase 4: Review & Next Steps

## Spec Complete

Once your specification is ready, you'll see:

```markdown
## Work System Spec Complete!

I've written your specification to: [file path]

The spec includes:
- [Summary of what was captured]
- [Key technical decisions]
- [Success metrics]
```

## Four Options

### Option 1: Review & Export
- Spec is ready for you to review and edit
- You can share it with teammates or use it in future conversations
- The spec is self-contained and explains the full system

### Option 2: Plan Implementation
- I'll enter plan mode to design the implementation approach
- This creates a step-by-step technical plan without executing yet
- Useful for complex systems or when you want to review before building
- I'll load the spec as context and design the architecture

### Option 3: Begin Implementation
- For simpler systems, we can start building immediately
- I'll follow the spec and keep you updated on progress
- Good when requirements are clear and system is straightforward

### Option 4: Iterate Further
- Re-run the interview on specific sections
- Add more detail or refine based on new insights
- Useful when you want to think more about certain aspects

## Implementation Handoff

When you choose to implement:

**Plan mode:** I'll provide context:
- Spec file location: [path]
- Key requirements: [summary]
- Technical constraints: [summary]
- Success metrics: [summary]

**Direct implementation:** I'll start building with regular spec references to ensure alignment.

---

# Phase 5: Iterative Refinement

## Updating Existing Specs

If you provide an existing spec file path, I'll:

1. **Read the current spec**
2. **Assess completeness:**
   - ✓ **Complete**: System Purpose, Success Metrics, Technical Stack
   - ⚠️ **Needs work**: Edge Cases (only 2 scenarios), Security (vague)
   - ❌ **Missing**: Data Model, Implementation Phases

3. **Ask what to focus on:**
   - Specific sections needing more detail?
   - New requirements or changes?
   - Expanding scope or adding features?

4. **Run targeted interview** (3-7 questions focused on that area)

5. **Update only relevant sections** (preserving existing content)

6. **Show summary of changes** using `scripts/compare_specs.py`

## Tracking Changes

The comparison script shows:
```markdown
## Spec Changes Summary

Modified sections:
- Edge Cases & Error Handling: Added 5 new scenarios
- Security & Privacy: Detailed access control model
- Data Model: Added complete entity-relationship diagram

Unchanged sections: 12
New sections: 1 (Data Model)
```

## Continuous Evolution

Work systems evolve. You can re-run this skill multiple times as you learn:
- After initial implementation (capture learnings)
- When adding features (update scope)
- After user feedback (refine workflows)
- When integrating new tools (update technical stack)

---

# Tips for Effective Interviews

## Listen for Complexity Signals

Adjust interview depth when you hear:
- "multiple user types" → Ask about roles, permissions, access patterns
- "integrate with X" → Ask about APIs, authentication, data sync
- "scale to Y" → Ask about performance, caching, async processing
- "compliance" → Ask about security, audit logs, data retention

## Provide Options for Technical Choices

Don't assume users know all options. When asking about tech stack:
- **Storage:** "Common options: SQLite (local, simple), Postgres (robust, scalable), or files (simplest)?"
- **Interface:** "CLI tool, web dashboard, Slack bot, or API for other tools?"
- **AI:** "Use Claude API, run local models, or no AI initially?"

## Flag Non-Goals Explicitly

Many project failures come from scope creep. Always ask:
- "What should this NOT do?"
- "What's out of scope for v1?"
- "What related problems are you NOT trying to solve?"

## Capture Success Metrics Early

This defines "done" and guides priorities:
- "How will you measure if this works?"
- "What's the main metric that matters?"
- "What would make you consider this a failure?"

## Adapt to User Style

- **Terse answers:** Ask more specific questions
- **Detailed answers:** Fewer questions needed, extract from narrative
- **Uncertain:** Provide examples and options
- **Technically deep:** Match technical depth

---

# References & Examples

## Question Framework
See [question-framework.md](./references/question-framework.md) for:
- Complete question catalog (50+ questions)
- When to use each question
- How to adapt follow-ups based on responses
- Question delivery best practices

## Spec Template
See [spec-template.md](./references/spec-template.md) for:
- Detailed template with instructions for each section
- What to include in each part of the spec
- Examples of well-written sections

## Example Specifications
- [task-management-spec.md](./references/examples/task-management-spec.md) - Personal task tracker
- [knowledge-management-spec.md](./references/examples/knowledge-management-spec.md) - Team wiki system
- [automation-workflow-spec.md](./references/examples/automation-workflow-spec.md) - Email to ticket automation

## Implementation Patterns
See [implementation-patterns.md](./references/implementation-patterns.md) for:
- Common architectural patterns (local-first, client-server, event-driven, hybrid)
- When to use each pattern
- Technology stack examples
- Pros/cons and complexity levels

---

# Getting Started

To begin, simply tell me:
1. Are you creating a new system or refining an existing spec?
2. Describe your work system in 1-3 sentences

I'll take it from there with a comprehensive interview that ensures we capture everything you need for successful implementation.
