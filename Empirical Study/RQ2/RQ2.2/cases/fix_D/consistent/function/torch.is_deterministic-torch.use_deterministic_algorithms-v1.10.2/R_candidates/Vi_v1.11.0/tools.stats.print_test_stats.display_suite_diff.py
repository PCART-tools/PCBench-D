def display_suite_diff(diff: SuiteDiff) -> str:
    lines = [f'class {diff["name"]}:']

    suite_fmt = ((4, 2), (3, 2))

    was = diff['was']
    if was:
        lines.append(f'    # was {display_stat(was, suite_fmt)}')

    now = diff['now']
    if now is not None:
        now_stat: Stat = {'center': now, 'spread': None}
        lines.append(f'    # now {display_stat(now_stat, suite_fmt)}')

    for case_diff in diff['cases']:
        lines.extend([f'  {l}' for l in case_diff_lines(case_diff)])

    return unlines([''] + [f'{diff["margin"]} {l}'.rstrip() for l in lines] + [''])
