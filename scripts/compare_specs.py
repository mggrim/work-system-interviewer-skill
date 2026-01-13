#!/usr/bin/env python3
"""
Work System Spec Comparator

Compares two versions of a work system specification and shows what changed.
Useful for iterative refinement to see exactly what was updated.

Usage:
    python compare_specs.py OLD_SPEC.md NEW_SPEC.md
    python compare_specs.py --help

Exit codes:
    0 - Files compared successfully (may or may not have differences)
    2 - File not found or invalid arguments
"""

import argparse
import difflib
import re
import sys
from pathlib import Path
from typing import Dict

# ANSI color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'


def parse_markdown_sections(content: str) -> Dict[str, str]:
    """
    Parse markdown content into sections based on ## headers.

    Returns dict mapping section names to their content.
    """
    sections = {}
    current_section = None
    current_content = []

    lines = content.split('\n')

    for line in lines:
        if line.startswith('## '):
            # Save previous section
            if current_section:
                sections[current_section] = '\n'.join(current_content)

            # Start new section
            current_section = line[3:].strip()
            current_content = []
        elif current_section:
            current_content.append(line)

    # Save last section
    if current_section:
        sections[current_section] = '\n'.join(current_content)

    return sections


def compare_sections(old_sections: Dict[str, str], new_sections: Dict[str, str]) -> Dict:
    """
    Compare sections between two spec versions.

    Returns dict with:
        - added: sections in new but not old
        - removed: sections in old but not new
        - modified: sections in both but with different content
        - unchanged: sections in both with same content
    """
    old_names = set(old_sections.keys())
    new_names = set(new_sections.keys())

    added = new_names - old_names
    removed = old_names - new_names
    common = old_names & new_names

    modified = []
    unchanged = []

    for name in common:
        old_content = old_sections[name].strip()
        new_content = new_sections[name].strip()

        if old_content != new_content:
            modified.append(name)
        else:
            unchanged.append(name)

    return {
        'added': sorted(added),
        'removed': sorted(removed),
        'modified': sorted(modified),
        'unchanged': sorted(unchanged),
    }


def show_section_diff(name: str, old_content: str, new_content: str, context_lines: int = 3):
    """Show unified diff for a section."""
    old_lines = old_content.strip().split('\n')
    new_lines = new_content.strip().split('\n')

    diff = difflib.unified_diff(
        old_lines,
        new_lines,
        fromfile='old',
        tofile='new',
        lineterm='',
        n=context_lines
    )

    print(f"\n{BOLD}{CYAN}{'─' * 60}{RESET}")
    print(f"{BOLD}{CYAN}Section: {name}{RESET}")
    print(f"{CYAN}{'─' * 60}{RESET}")

    has_changes = False
    for line in diff:
        if line.startswith('---') or line.startswith('+++'):
            # Skip file headers
            continue
        elif line.startswith('@@'):
            # Hunk header
            print(f"{CYAN}{line}{RESET}")
            has_changes = True
        elif line.startswith('+'):
            # Addition
            print(f"{GREEN}{line}{RESET}")
        elif line.startswith('-'):
            # Deletion
            print(f"{RED}{line}{RESET}")
        else:
            # Context
            print(line)

    if not has_changes:
        print(f"{YELLOW}(No differences found - this shouldn't happen){RESET}")


def print_summary(comparison: Dict, old_file: str, new_file: str):
    """Print summary of changes."""
    print(f"\n{BOLD}{'═' * 60}{RESET}")
    print(f"{BOLD}Spec Comparison Summary{RESET}")
    print(f"{'═' * 60}")
    print(f"Old: {old_file}")
    print(f"New: {new_file}")
    print(f"{'═' * 60}\n")

    # Added sections
    if comparison['added']:
        print(f"{GREEN}{BOLD}➕ New Sections ({len(comparison['added'])}){RESET}")
        for name in comparison['added']:
            print(f"   {GREEN}+ {name}{RESET}")
        print()

    # Removed sections
    if comparison['removed']:
        print(f"{RED}{BOLD}➖ Removed Sections ({len(comparison['removed'])}){RESET}")
        for name in comparison['removed']:
            print(f"   {RED}- {name}{RESET}")
        print()

    # Modified sections
    if comparison['modified']:
        print(f"{YELLOW}{BOLD}📝 Modified Sections ({len(comparison['modified'])}){RESET}")
        for name in comparison['modified']:
            print(f"   {YELLOW}~ {name}{RESET}")
        print()

    # Unchanged sections
    if comparison['unchanged']:
        print(f"{BOLD}✓ Unchanged Sections ({len(comparison['unchanged'])}){RESET}")
        for name in comparison['unchanged']:
            print(f"   ✓ {name}")
        print()

    # Overall summary
    total_sections = len(comparison['added']) + len(comparison['removed']) + \
                    len(comparison['modified']) + len(comparison['unchanged'])
    changed_sections = len(comparison['added']) + len(comparison['removed']) + \
                      len(comparison['modified'])

    print(f"{'─' * 60}")
    print(f"{BOLD}Total sections:{RESET} {total_sections}")
    print(f"{BOLD}Changed sections:{RESET} {changed_sections}")

    if changed_sections == 0:
        print(f"\n{GREEN}{BOLD}✓ No changes detected. Specs are identical.{RESET}")
    else:
        print(f"\n{YELLOW}{BOLD}⚡ {changed_sections} section(s) changed.{RESET}")


def main():
    parser = argparse.ArgumentParser(
        description='Compare two work system specification files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python compare_specs.py old-spec.md new-spec.md
    python compare_specs.py v1-spec.md v2-spec.md --detailed

This tool:
    - Identifies new, removed, and modified sections
    - Shows unified diffs for modified sections
    - Provides summary of all changes
        """
    )

    parser.add_argument('old_spec', type=str, help='Path to old/original spec file')
    parser.add_argument('new_spec', type=str, help='Path to new/updated spec file')
    parser.add_argument('--detailed', '-d', action='store_true',
                       help='Show detailed diffs for all modified sections')
    parser.add_argument('--context', '-c', type=int, default=3,
                       help='Number of context lines in diffs (default: 3)')

    args = parser.parse_args()

    # Check files exist
    old_path = Path(args.old_spec)
    new_path = Path(args.new_spec)

    if not old_path.exists():
        print(f"{RED}Error: Old spec file not found: {old_path}{RESET}", file=sys.stderr)
        return 2

    if not new_path.exists():
        print(f"{RED}Error: New spec file not found: {new_path}{RESET}", file=sys.stderr)
        return 2

    # Read files
    try:
        old_content = old_path.read_text(encoding='utf-8')
        new_content = new_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"{RED}Error reading files: {e}{RESET}", file=sys.stderr)
        return 2

    # Parse sections
    old_sections = parse_markdown_sections(old_content)
    new_sections = parse_markdown_sections(new_content)

    # Compare
    comparison = compare_sections(old_sections, new_sections)

    # Print summary
    print_summary(comparison, str(old_path), str(new_path))

    # Show detailed diffs if requested
    if args.detailed and comparison['modified']:
        print(f"\n{BOLD}{'═' * 60}{RESET}")
        print(f"{BOLD}Detailed Diffs for Modified Sections{RESET}")
        print(f"{'═' * 60}\n")

        for name in comparison['modified']:
            show_section_diff(
                name,
                old_sections[name],
                new_sections[name],
                context_lines=args.context
            )

        print(f"\n{BOLD}{CYAN}{'═' * 60}{RESET}\n")

    # Show content of new sections
    if comparison['added']:
        print(f"\n{BOLD}{'═' * 60}{RESET}")
        print(f"{BOLD}Content of New Sections{RESET}")
        print(f"{'═' * 60}\n")

        for name in comparison['added']:
            print(f"{BOLD}{GREEN}Section: {name}{RESET}")
            print(f"{GREEN}{'─' * 60}{RESET}")
            content = new_sections[name].strip()
            # Show first 10 lines or full content if shorter
            lines = content.split('\n')[:10]
            print('\n'.join(lines))
            total_lines = len(new_sections[name].split('\n'))
            if total_lines > 10:
                remaining_lines = total_lines - 10
                print(f"{GREEN}... ({remaining_lines} more lines){RESET}")
            print()

    return 0


if __name__ == '__main__':
    sys.exit(main())
