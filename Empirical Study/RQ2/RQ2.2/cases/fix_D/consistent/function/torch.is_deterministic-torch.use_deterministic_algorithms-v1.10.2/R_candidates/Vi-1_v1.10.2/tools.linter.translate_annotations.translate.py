def translate(diff: Diff, line_number: int) -> Optional[int]:
    if line_number < 1:
        return None

    hunks = diff['hunks']
    if not hunks:
        return line_number

    keyified = KeyifyList(
        hunks,
        lambda hunk: hunk['new_start'] + (0 if hunk['new_count'] > 0 else 1)
    )
    i = bisect_right(cast(Sequence[int], keyified), line_number)
    if i < 1:
        return line_number

    hunk = hunks[i - 1]
    d = line_number - (hunk['new_start'] + (hunk['new_count'] or 1))
    return None if d < 0 else hunk['old_start'] + (hunk['old_count'] or 1) + d
