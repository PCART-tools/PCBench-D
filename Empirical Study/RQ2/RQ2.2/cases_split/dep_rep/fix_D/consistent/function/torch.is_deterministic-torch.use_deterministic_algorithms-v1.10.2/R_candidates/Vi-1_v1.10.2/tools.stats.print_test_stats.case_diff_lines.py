def case_diff_lines(diff: CaseDiff) -> List[str]:
    lines = [f'def {diff["name"]}: ...']

    case_fmt = ((3, 3), (2, 3))

    was = diff['was']
    if was:
        was_line = f'    # was {display_stat(was[0], case_fmt)}'
        was_status = was[1]
        if was_status:
            was_line += f' ({was_status})'
        lines.append(was_line)

    now = diff['now']
    if now:
        now_stat: Stat = {'center': now['seconds'], 'spread': None}
        now_line = f'    # now {display_stat(now_stat, case_fmt)}'
        now_status = now['status']
        if now_status:
            now_line += f' ({now_status})'
        lines.append(now_line)

    return [''] + [f'{diff["margin"]} {l}' for l in lines]
