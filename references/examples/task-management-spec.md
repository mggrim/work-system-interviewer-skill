# DevTask - Personal Task Tracker

## Overview

- **Purpose**: Track and manage development tasks for personal software projects with automatic prioritization
- **Last Updated**: 2026-01-13
- **Status**: Ready for Implementation

## System Scope

### In Scope

- Track bugs, features, chores, and research tasks for personal dev projects
- Simple P0-P3 priority system with automatic tagging
- Local SQLite storage for fast access and privacy
- CLI interface for quick task entry and viewing
- Filter and search tasks by type, priority, project, tags
- Basic time tracking (start/stop timer on tasks)

### Explicitly Out of Scope (Non-Goals)

- NOT a team collaboration tool (single user only)
- NOT replacing GitHub Issues for open source projects
- NOT providing a web interface (CLI only for v1)
- NOT syncing across devices (local only for now)
- NOT handling dependencies between tasks

## User Profiles

### Primary Users

- **Solo Developer** (1 person - me): Creates tasks throughout the day as I work on personal projects. Views task list multiple times per day. Primarily uses during focused work sessions.

### Technical Level

**Advanced** - Comfortable with CLI tools, SQLite, Python scripts. Prefers keyboard-driven interfaces over GUI. Familiar with command composition and piping.

## Work Flow

### Input & Capture

#### Entry Points

- **CLI Command**: `devtask add "Fix login bug" --type bug --project auth-service` (primary method)
- **Quick Add**: `devtask add "Research Redis caching"` (minimal, system infers details)
- **Batch Import**: `devtask import tasks.txt` (for migrating from old TODO list)

#### Required Metadata

- **Title** (required, text, user-provided): What needs to be done
- **Type** (required, enum [bug|feature|chore|research], auto-detected or user-set): Category of work
- **Priority** (optional, P0-P3, auto-calculated): Urgency level
- **Project** (optional, text, user-provided): Which codebase/project
- **Tags** (optional, list, user-provided): Free-form labels
- **Created** (required, timestamp, auto): When task was added
- **ID** (required, int, auto): Unique identifier

#### Work Types

- **Bug**: Something broken. Keywords: "fix", "bug", "broken", "crash", "error". Auto-tagged with P1 priority.
- **Feature**: New functionality. Keywords: "add", "build", "implement". Auto-tagged with P2 priority.
- **Chore**: Maintenance work. Keywords: "refactor", "update", "cleanup". Auto-tagged with P2 priority.
- **Research**: Investigation or learning. Keywords: "research", "explore", "learn", "investigate". Auto-tagged with P3 priority.

### Processing & Organization

#### Categorization Logic

- **Automatic Type Detection**: NLP keyword matching in title. If keywords found → set type. If ambiguous or no keywords → prompt user to clarify.
- **Manual Override**: User can always explicitly set type with `--type` flag.
- **Project Assignment**: Manual via `--project` flag. Projects are freeform strings (not predefined list).

#### Priority Framework

- **P0 (Critical)**: Blocking all work. Manually set only. E.g., "Can't run dev server"
- **P1 (High)**: Important, should do soon. Auto-set for bugs. E.g., "Fix broken login"
- **P2 (Normal)**: Standard work. Auto-set for features and chores. E.g., "Add dark mode"
- **P3 (Low)**: Nice to have, when time permits. Auto-set for research. E.g., "Explore GraphQL"
- **Age-based Escalation**: P3 tasks older than 30 days auto-escalate to P2. P2 tasks older than 60 days flagged for review (maybe not important?).

#### Workflow States

1. **Open**: New task, not started (default on creation)
2. **In Progress**: Currently working on it (set with `devtask start <id>`, starts timer)
3. **Blocked**: Can't proceed, waiting on something (set with `devtask block <id> --reason "..."`)
4. **Done**: Completed (set with `devtask done <id>`, stops timer)

Transitions:
- Open → In Progress: `devtask start <id>`
- In Progress → Blocked: `devtask block <id>`
- Blocked → In Progress: `devtask unblock <id>`
- In Progress → Done: `devtask done <id>`
- Any → Done: `devtask done <id>` (can complete without starting)

#### Automation Rules

- **Auto-type Detection**: On add without `--type`, scan title for keywords and suggest type. If confident (1 keyword match), auto-set. If uncertain, prompt.
- **Auto-priority Assignment**: Based on type. Bug→P1, Feature/Chore→P2, Research→P3.
- **Age Escalation**: Daily cron job checks task ages. P3 tasks 30+ days old → P2. P2 tasks 60+ days old → Add `needs-review` tag.
- **Timer Auto-stop**: If a task "In Progress" for >8 hours without activity, auto-pause timer and add note (in case I forgot to stop it).

### Output & Interaction

#### User Interface

- **Primary**: Command-line interface (CLI) using Python Click framework
- **Commands**:
  - `devtask add "title" [--type T] [--project P] [--priority PX]` - Create task
  - `devtask list [--type T] [--priority PX] [--project P]` - View tasks
  - `devtask show <id>` - View task details
  - `devtask start <id>` - Start working (sets "In Progress", starts timer)
  - `devtask done <id>` - Mark complete (stops timer if running)
  - `devtask block <id> --reason "..."` - Mark blocked
  - `devtask search <query>` - Full-text search
  - `devtask stats` - Show summary (tasks by type, time spent, etc.)

#### Key Actions

- **Add Task**: Creates new task in database with auto-detection
- **List Tasks**: Shows table of matching tasks (ID, Title, Type, Priority, Project). Color-coded by priority.
- **Start Task**: Sets status to "In Progress", records start time for time tracking
- **Complete Task**: Sets status to "Done", records completion time, stops timer
- **Block Task**: Sets status to "Blocked", prompts for reason, adds note
- **Search**: Full-text search across titles and any notes

#### Notifications/Alerts

- **None in v1**: CLI-only, no notifications. Check list manually.
- **Future**: Optional daily summary email or Slack message (not implementing yet)

## Technical Architecture

### Technology Stack

- **CLI**: Python 3.11+ with Click framework for command parsing
- **Database**: SQLite 3 (local file at `~/.devtask/tasks.db`)
- **NLP**: Simple keyword matching (regex), no ML models
- **Configuration**: TOML file at `~/.devtask/config.toml` for preferences
- **Deployment**: Single Python script, installed via `pip install -e .` or `pipx`

### Data Model

**tasks** table:
- id (INTEGER PRIMARY KEY)
- title (TEXT NOT NULL)
- type (TEXT CHECK(type IN ('bug','feature','chore','research')))
- priority (TEXT CHECK(priority IN ('P0','P1','P2','P3')))
- status (TEXT CHECK(status IN ('open','in_progress','blocked','done')))
- project (TEXT)
- tags (TEXT) -- comma-separated for simplicity
- created_at (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
- started_at (TIMESTAMP)
- completed_at (TIMESTAMP)
- blocked_reason (TEXT)
- time_spent_seconds (INTEGER DEFAULT 0) -- accumulated time

**time_logs** table:
- id (INTEGER PRIMARY KEY)
- task_id (INTEGER REFERENCES tasks(id))
- start_time (TIMESTAMP)
- end_time (TIMESTAMP)
- duration_seconds (INTEGER)

### AI/Automation Components

**Auto-type Detection**:
- Simple keyword matching (no LLM needed)
- Keywords dict: `{"bug": ["fix", "bug", "broken"], "feature": ["add", "build"], ...}`
- If title contains keyword → suggest that type
- No fallback needed (just prompt user if uncertain)

**No external APIs**: Fully offline, local-only processing.

## Edge Cases & Error Handling

**Scenario 1: Ambiguous type (title matches multiple keyword sets)**
- **Handling**: Prompt user with suggestions: "Title matches both 'bug' and 'feature'. Which type? [b/f]"

**Scenario 2: Database locked (SQLite file in use)**
- **Handling**: Retry 3 times with 100ms delay. If still locked, show error: "Database busy. Try again in a moment."

**Scenario 3: Task timer running when starting another task**
- **Handling**: Auto-stop previous timer, prompt: "Stopped timer on task #123. Now starting #124."

**Scenario 4: Marking task done but timer never started**
- **Handling**: Allow it. Time spent = 0. Some tasks completed quickly without explicit "start".

**Scenario 5: Batch import with malformed lines**
- **Handling**: Skip invalid lines, log to stderr, continue with valid ones. Show summary: "Imported 45/50 tasks. 5 skipped (see errors above)."

## Security & Privacy Considerations

**Data Sensitivity**:
- Task titles may contain sensitive info (client names, proprietary features)
- All data stored locally in `~/.devtask/` directory

**Access Control**:
- Single user system (no auth needed)
- File permissions: `~/.devtask/` directory set to 700 (owner-only access)

**Data Protection**:
- No encryption (local-only, trust OS file permissions)
- No network requests (no data leaves machine)
- SQLite database at `~/.devtask/tasks.db` with restrictive permissions (600)

**Backups**:
- User responsible for backing up `~/.devtask/` directory
- Could add `devtask export` command to dump to JSON for manual backups

## Success Metrics

### Primary Metric

**Daily Task Completion Rate**: Tasks marked "done" per day.
- **Target**: Average 5+ tasks/day (currently averaging ~2/day with scattered TODO lists)
- **Measurement**: Query database for completed tasks per day, track 30-day rolling average

### Secondary Metrics

- **Time to Capture**: How quickly I can add a task (should be <10 seconds with quick add)
- **Active Task Count**: Number of open/in-progress tasks (target: keep under 20 to avoid overwhelm)
- **Age of Oldest Task**: Catch stale tasks (flag if P0/P1 task is >7 days old)
- **Time Spent per Type**: See where time goes (expect bugs=30%, features=50%, chores=10%, research=10%)

### Failure Indicators

- **Low capture rate**: If I'm still keeping paper notes or separate TODO lists → system too cumbersome
- **Many stale tasks**: If 50%+ of tasks are >30 days old → either bad prioritization or capturing too much
- **Not using it daily**: If I go 3+ days without interacting → not habit-forming, needs improvement
- **Time tracking ignored**: If I never use `start`/`done` timer → feature not valuable, remove to simplify

## Implementation Notes

### Phase 1: MVP (Target: 1 week)

- Core CLI: add, list, show, done
- SQLite database with tasks table
- Auto-type detection (simple keywords)
- Priority assignment (based on type)
- Status workflow (open → done)

### Phase 2: Time Tracking (Target: +3 days)

- Add start/stop commands
- time_logs table for tracking
- Timer auto-stop after 8 hours
- `devtask stats` showing time per task/type

### Phase 3: Enhancements (Target: +1 week)

- Block/unblock with reasons
- Search command
- Age-based escalation (cron job)
- Export to JSON
- Configuration file for keywords, escalation thresholds

### Dependencies

- Python 3.11+ installed
- SQLite 3 (included with Python)
- Click library: `pip install click`
- Rich library (optional): `pip install rich` for colored output

## Open Questions

None - ready to implement.

## Interview Context

This specification was developed through a structured interview on 2026-01-13.
Key decisions:
- Chose CLI over web interface for speed and simplicity (can add web later)
- Decided on simple keyword matching instead of LLM to keep it fast and offline
- Opted for SQLite over files for query flexibility and data integrity
- P0-P3 priority instead of numeric or other systems (familiar from work experience)
