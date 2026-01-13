#!/usr/bin/env python3
"""
Work System Spec Validator

Validates completeness of work system specification markdown files.
Checks for required sections and flags empty or incomplete sections.

Usage:
    python validate_spec.py SPEC_FILE.md
    python validate_spec.py --help

Exit codes:
    0 - Spec is complete
    1 - Spec has issues (missing or incomplete sections)
    2 - File not found or invalid
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# ANSI color codes for output
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

# Required sections and their minimum content length (chars)
REQUIRED_SECTIONS = {
    'Overview': 50,
    'System Scope': 100,
    'User Profiles': 50,
    'Work Flow': 200,
    'Technical Architecture': 100,
    'Edge Cases & Error Handling': 100,
    'Success Metrics': 100,
}

# Optional but recommended sections
RECOMMENDED_SECTIONS = {
    'Security & Privacy Considerations': 50,
    'Implementation Notes': 50,
    'Interview Context': 20,
}


def parse_markdown_sections(content: str) -> Dict[str, str]:
    """
    Parse markdown content into sections based on headers.

    Returns dict mapping section names to their content (everything until next same-level header).
    """
    sections = {}
    current_section = None
    current_content = []

    lines = content.split('\n')

    for line in lines:
        # Check for ## level headers (top-level sections in spec)
        if line.startswith('## '):
            # Save previous section
            if current_section:
                sections[current_section] = '\n'.join(current_content).strip()

            # Start new section
            current_section = line[3:].strip()
            current_content = []
        elif current_section:
            current_content.append(line)

    # Save last section
    if current_section:
        sections[current_section] = '\n'.join(current_content).strip()

    return sections


def clean_content(content: str) -> str:
    """Remove HTML comments and empty lines for content length calculation."""
    # Remove HTML comments
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    # Remove lines that are just dashes or equals (markdown separators)
    content = re.sub(r'^[-=]+$', '', content, flags=re.MULTILINE)
    # Remove extra whitespace
    content = re.sub(r'\n\s*\n', '\n', content)
    return content.strip()


def validate_section(name: str, content: str, min_length: int) -> Tuple[str, str]:
    """
    Validate a single section.

    Returns tuple of (status, message) where status is 'complete', 'incomplete', or 'missing'.
    """
    if not content:
        return 'missing', f'Section not found'

    cleaned = clean_content(content)

    if len(cleaned) < min_length:
        return 'incomplete', f'Only {len(cleaned)} chars (min: {min_length}). Needs more detail.'

    # Check for placeholder text that suggests incomplete section
    placeholders = ['[TODO]', '[TBD]', '[Fill this in]', '[Description]', '[Example]']
    if any(placeholder.lower() in cleaned.lower() for placeholder in placeholders):
        return 'incomplete', 'Contains placeholder text'

    return 'complete', 'OK'


def print_results(results: Dict[str, Tuple[str, str, bool]],
                 title: str = "Section Validation Results"):
    """Print validation results with colored output."""
    print(f"\n{BOLD}{title}{RESET}")
    print("=" * 60)

    complete_count = 0
    incomplete_count = 0
    missing_count = 0

    for section_name, (status, message, required) in results.items():
        req_mark = "*" if required else " "

        if status == 'complete':
            icon = f"{GREEN}✓{RESET}"
            complete_count += 1
        elif status == 'incomplete':
            icon = f"{YELLOW}⚠{RESET}"
            incomplete_count += 1
        else:  # missing
            icon = f"{RED}❌{RESET}"
            missing_count += 1

        print(f"{icon} {req_mark}{section_name:<40} {message}")

    print("\n" + "=" * 60)
    print(f"{BOLD}Summary:{RESET}")
    print(f"  {GREEN}✓{RESET} Complete: {complete_count}")
    if incomplete_count > 0:
        print(f"  {YELLOW}⚠{RESET} Incomplete: {incomplete_count}")
    if missing_count > 0:
        print(f"  {RED}❌{RESET} Missing: {missing_count}")

    required_total = sum(1 for _, _, req in results.values() if req)
    required_complete = sum(1 for status, _, req in results.values()
                           if req and status == 'complete')

    print(f"\n  Required sections: {required_complete}/{required_total}")

    if missing_count == 0 and incomplete_count == 0:
        print(f"\n{GREEN}{BOLD}🎉 Spec is complete and ready for implementation!{RESET}")
        return True
    else:
        print(f"\n{YELLOW}{BOLD}⚡ Spec needs work before implementation.{RESET}")
        if missing_count > 0:
            print(f"   - {missing_count} section(s) missing")
        if incomplete_count > 0:
            print(f"   - {incomplete_count} section(s) incomplete")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Validate work system specification markdown files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python validate_spec.py my-work-system-spec.md
    python validate_spec.py ~/projects/specs/task-tracker-spec.md

Required Sections:
    """ + "\n    ".join(f"- {name}" for name in REQUIRED_SECTIONS.keys()) + """

Recommended Sections:
    """ + "\n    ".join(f"- {name}" for name in RECOMMENDED_SECTIONS.keys())
    )

    parser.add_argument('spec_file', type=str, help='Path to spec markdown file')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show section content lengths')

    args = parser.parse_args()

    # Check file exists
    spec_path = Path(args.spec_file)
    if not spec_path.exists():
        print(f"{RED}Error: File not found: {spec_path}{RESET}", file=sys.stderr)
        return 2

    if not spec_path.is_file():
        print(f"{RED}Error: Not a file: {spec_path}{RESET}", file=sys.stderr)
        return 2

    # Read and parse spec
    print(f"Validating: {BOLD}{spec_path}{RESET}")

    try:
        content = spec_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"{RED}Error reading file: {e}{RESET}", file=sys.stderr)
        return 2

    sections = parse_markdown_sections(content)

    if args.verbose:
        print(f"\nFound {len(sections)} sections:")
        for name, content in sections.items():
            cleaned = clean_content(content)
            print(f"  - {name}: {len(cleaned)} chars")

    # Validate required sections
    results = {}

    for section_name, min_length in REQUIRED_SECTIONS.items():
        content = sections.get(section_name, '')
        status, message = validate_section(section_name, content, min_length)
        results[section_name] = (status, message, True)  # True = required

    # Validate recommended sections
    for section_name, min_length in RECOMMENDED_SECTIONS.items():
        content = sections.get(section_name, '')
        status, message = validate_section(section_name, content, min_length)
        results[section_name] = (status, message, False)  # False = recommended

    # Print results
    is_complete = print_results(results)

    # Note about asterisks
    print(f"\n{BOLD}Note:{RESET} * indicates required sections\n")

    # Exit with appropriate code
    return 0 if is_complete else 1


if __name__ == '__main__':
    sys.exit(main())
