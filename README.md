# Work System Interviewer

A [Claude Code](https://claude.ai/code) skill for designing AI-based work systems through comprehensive structured interviews.

## Overview

This skill guides users through 8-15+ structured questions to design systems for organizing and executing incoming work. It generates comprehensive specifications ready for implementation, covering task management, knowledge management, automation workflows, and communication/collaboration systems.

## Features

- **Comprehensive Interview**: 8-15+ questions across 7 categories (Purpose, Input, Processing, Output, Technical, Edge Cases, Success Metrics)
- **Structured Specs**: Generates detailed markdown specifications with 15+ sections
- **Iterative Refinement**: Update existing specs with targeted questions
- **Validation Tools**: Python scripts to check completeness and compare versions
- **Implementation Guidance**: 4 architectural patterns with technology recommendations
- **Real Examples**: 3 complete example specifications (task tracker, team wiki, email automation)

## Installation

### For Claude Code

1. Clone this repository into your Claude Code skills directory:

```bash
cd ~/.claude/skills
git clone https://github.com/mggrim/work-system-interviewer-skill.git work-system-interviewer
```

2. Restart Claude Code or VS Code to load the skill

3. Trigger the skill by asking Claude to "design a work system" or "create a task management approach"

### Verification

Test that the skill is installed correctly:

```bash
# Check the skill exists
ls ~/.claude/skills/work-system-interviewer/SKILL.md

# Test the validation script
python3 ~/.claude/skills/work-system-interviewer/scripts/validate_spec.py --help
```

## Usage

### Creating a New Work System

Simply ask Claude Code to help design your system:

```
"Help me design a work system for managing customer support requests"
```

The skill will:
1. Gather initial context about your system
2. Interview you with 8-15+ targeted questions
3. Generate a comprehensive specification
4. Offer next steps (review, plan implementation, or iterate)

### Refining an Existing Spec

If you have an existing specification and want to improve it:

```
"I have a work system spec at ./my-spec.md. Help me refine the edge cases section."
```

### Example Questions Covered

The interview covers:

- **System Purpose & Scope**: What's in/out, non-goals
- **Input & Triggers**: How work enters the system
- **Processing & Organization**: Workflows, automation, categorization
- **Output & Action**: User interface, key actions
- **Technical Implementation**: Stack, integrations, scale requirements
- **Edge Cases & Concerns**: Failure modes, error handling
- **Success Metrics**: How to measure success

## Tools Included

### validate_spec.py

Validates that a work system spec is complete and ready for implementation.

```bash
python3 scripts/validate_spec.py path/to/spec.md
```

Output:
- ✓ Complete sections
- ⚠️ Incomplete sections (need more detail)
- ❌ Missing sections

### compare_specs.py

Compares two versions of a spec to see what changed.

```bash
python3 scripts/compare_specs.py old-spec.md new-spec.md --detailed
```

Shows:
- New sections added
- Sections removed
- Modified sections with diffs
- Unchanged sections

## Examples

The skill includes three complete example specifications:

### 1. DevTask - Personal Task Tracker
- CLI tool for solo developer
- Local SQLite storage
- Auto-categorization and priority
- Time tracking

### 2. TeamKnowledge - Team Wiki System
- Multi-user web application
- AI-powered semantic search
- Slack bot integration
- Version history

### 3. SupportRouter - Email Automation
- Event-driven serverless architecture
- AWS Lambda + SES email processing
- AI categorization with Claude
- Smart routing to team members

View examples in [`references/examples/`](./references/examples/)

## Implementation Patterns

The skill provides guidance on 4 common architectural patterns:

1. **Local-First**: Single-user, offline, fast (SQLite, CLI)
2. **Client-Server**: Multi-user, web-based (React, Node.js, PostgreSQL)
3. **Event-Driven**: Automation-focused, high-volume (Lambda, SQS, webhooks)
4. **Hybrid**: Local + cloud sync for multi-device access

See [`references/implementation-patterns.md`](./references/implementation-patterns.md) for details.

## File Structure

```
work-system-interviewer/
├── SKILL.md                    # Main skill definition (429 lines)
├── LICENSE.txt                 # Apache 2.0 license
├── scripts/
│   ├── validate_spec.py        # Validate spec completeness
│   └── compare_specs.py        # Diff two spec versions
├── references/
│   ├── question-framework.md   # Complete question catalog (200+ lines)
│   ├── spec-template.md        # Detailed template (150+ lines)
│   ├── implementation-patterns.md # Architecture patterns guide
│   └── examples/
│       ├── task-management-spec.md
│       ├── knowledge-management-spec.md
│       └── automation-workflow-spec.md
```

## Use Cases

This skill is ideal for:

- **Developers** building personal productivity tools
- **Teams** designing internal work management systems
- **Product Managers** speccing new workflow automation
- **Engineers** architecting task processing pipelines
- **Consultants** helping clients organize work systems

## How It Works

1. **Adaptive Interviewing**: Asks 8-15+ questions based on system complexity
2. **Provides Options**: Suggests technologies when users may not know choices
3. **Captures Non-Goals**: Explicitly defines what's out of scope to prevent creep
4. **Success First**: Defines metrics upfront to clarify "done"
5. **Edge Case Focused**: Ensures robustness by thinking through failures

## Requirements

- Claude Code (VS Code extension or CLI)
- Python 3.8+ (for validation/comparison scripts)

## Contributing

Contributions welcome! Areas for improvement:

- Additional example specifications
- More implementation patterns
- Enhanced validation rules
- Support for different spec formats (YAML, JSON)

## License

Apache 2.0 - See [LICENSE.txt](./LICENSE.txt)

## Credits

Created using Claude Code and the [skill-creator skill](https://github.com/anthropics/skills/tree/main/skills/skill-creator) from Anthropic.

## Related

- [Anthropic Skills Repository](https://github.com/anthropics/skills) - Official collection of Claude Code skills
- [Claude Code Documentation](https://code.claude.com/docs) - Learn more about building with Claude Code
- [Agent Skills Specification](https://github.com/anthropics/skills/tree/main/spec) - Technical details on skill format
