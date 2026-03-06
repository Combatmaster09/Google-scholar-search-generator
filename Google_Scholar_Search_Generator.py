#!/usr/bin/env python3
"""Google Scholar search query generator.

Collects groups of required terms (with optional alternate names) and
exclusion phrases, then builds a query string such as:

    ("mass panic" OR "crowd panic") AND ("rational" OR "irrational") -"not peer reviewed" -"not peer-reviewed"

Usage: run the script and follow prompts. Enter '-' to finish lists.
"""

from typing import List


def _quote_term(t: str) -> str:
    t = t.strip()
    if not t:
        return ''
    # Always wrap terms in quotes, unless already wrapped
    if t.startswith('"') and t.endswith('"'):
        return t
    return f'"{t}"'


def _format_group(group: List[str]) -> str:
    terms = [_quote_term(x) for x in group if x and x.strip()]
    if not terms:
        return ''
    if len(terms) == 1:
        return terms[0]
    return '(' + ' OR '.join(terms) + ')'


def build_query(groups: List[List[str]], excludes: List[str]) -> str:
    """Build the final query string from groups and excludes.

    - groups: list of lists, each inner list contains a required term and its alternates
    - excludes: list of phrases to exclude
    """
    group_parts = [p for p in (_format_group(g) for g in groups) if p]
    main = ' AND '.join(group_parts)

    # Default phrases to always exclude
    default_excludes = [
        'not peer reviewed',
        'not peer-reviewed',
        'non peer reviewed',
        'non peer-reviewed',
    ]

    # Merge user excludes with defaults while preserving order and removing empties
    merged = [e.strip() for e in excludes if e and e.strip()]
    for d in default_excludes:
        if d not in merged:
            merged.append(d)

    exclude_parts = [f'-{_quote_term(e)}' for e in merged]

    parts = []
    if main:
        parts.append(main)
    if exclude_parts:
        parts.append(' '.join(exclude_parts))

    if parts:
        return ' '.join(parts) + ' after:2015-12-31'
    return 'after:2015-12-31'


def collect_interactive() -> str:
    print('Enter required search terms. Enter "-" to finish.')
    groups: List[List[str]] = []
    while True:
        primary = input('Primary required term: ').strip()
        if primary == "-":
            break
        alt_line = input("Alternate names separated by ',': ").strip()
        alts = [s.strip() for s in alt_line.split(',') if s.strip()] if alt_line and alt_line != "-" else []
        groups.append([primary] + alts)

    print('\nEnter exclusion phrases (these will be prefixed with a minus). Enter "-" to finish.')
    excludes: List[str] = []
    while True:
        ex = input('Exclude phrase: ').strip()
        if ex == "-":
            break
        excludes.append(ex)

    query = build_query(groups, excludes)
    print('\nGenerated query:')
    print(query)
    return query


if __name__ == '__main__':
    while True:
        collect_interactive()
        choice = input("\nDo you want to create a new query? (y/n): ").strip().lower()
        if choice != 'y':
            break