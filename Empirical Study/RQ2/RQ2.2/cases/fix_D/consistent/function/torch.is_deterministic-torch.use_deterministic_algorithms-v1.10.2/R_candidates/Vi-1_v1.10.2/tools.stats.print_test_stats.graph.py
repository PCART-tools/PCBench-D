def graph(
    *,
    head_sha: Commit,
    head_seconds: float,
    base_seconds: Dict[Commit, List[float]],
    on_master: bool,
    ancestry_path: int = 0,
    other_ancestors: int = 0,
) -> str:
    lines = [
        'Commit graph (base is most recent master ancestor with at least one S3 report):',
        '',
        '    : (master)',
        '    |',
    ]

    head_time_str = f'           {format_seconds([head_seconds])}'
    if on_master:
        lines.append(f'    * {head_sha[:10]} (HEAD)   {head_time_str}')
    else:
        lines.append(f'    | * {head_sha[:10]} (HEAD) {head_time_str}')

        if ancestry_path > 0:
            lines += [
                '    | |',
                show_ancestors(ancestry_path),
            ]

        if other_ancestors > 0:
            lines += [
                '    |/|',
                show_ancestors(other_ancestors),
                '    |',
            ]
        else:
            lines.append('    |/')

    is_first = True
    for sha, seconds in base_seconds.items():
        num_runs = len(seconds)
        prefix = str(num_runs).rjust(3)
        base = '(base)' if is_first and num_runs > 0 else '      '
        if num_runs > 0:
            is_first = False
        t = format_seconds(seconds)
        p = plural(num_runs)
        if t:
            p = f'{p}, '.ljust(3)
        lines.append(f'    * {sha[:10]} {base} {prefix} report{p}{t}')

    lines.extend(['    |', '    :'])

    return unlines(lines)
