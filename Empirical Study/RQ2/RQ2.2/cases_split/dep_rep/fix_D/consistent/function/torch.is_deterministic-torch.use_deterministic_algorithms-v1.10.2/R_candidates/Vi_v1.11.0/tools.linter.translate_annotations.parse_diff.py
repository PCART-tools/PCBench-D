def parse_diff(diff: str) -> Diff:
    name = None
    name_found = False
    hunks: List[Hunk] = []
    for line in diff.splitlines():
        hunk_match = re.match(hunk_pattern, line)
        if name_found:
            if hunk_match:
                old_start, old_count, new_start, new_count = hunk_match.groups()
                hunks.append({
                    'old_start': int(old_start),
                    'old_count': int(old_count or '1'),
                    'new_start': int(new_start),
                    'new_count': int(new_count or '1'),
                })
        else:
            assert not hunk_match
            name_match = re.match(r'^--- (?:(?:/dev/null)|(?:a/(.*)))$', line)
            if name_match:
                name_found = True
                name, = name_match.groups()
    return {
        'old_filename': name,
        'hunks': hunks,
    }
