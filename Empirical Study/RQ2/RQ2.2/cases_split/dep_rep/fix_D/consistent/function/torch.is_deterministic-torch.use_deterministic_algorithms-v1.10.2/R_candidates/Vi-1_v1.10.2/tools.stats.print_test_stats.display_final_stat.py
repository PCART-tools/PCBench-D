def display_final_stat(stat: Stat) -> str:
    center = stat['center']
    spread = stat['spread']
    displayed = display_stat(
        {'center': abs(center), 'spread': spread},
        ((4, 2), (3, 2)),
    )
    if center < 0:
        sign = '-'
    elif center > 0:
        sign = '+'
    else:
        sign = ' '
    return f'{sign}{displayed}'.rstrip()
