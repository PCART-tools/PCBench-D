def display_stat(
    x: Stat,
    format: Tuple[Tuple[int, int], Tuple[int, int]],
) -> str:
    spread_len = format[1][0] + 1 + format[1][1]
    spread = x['spread']
    if spread is not None:
        spread_str = f' ± {spread:{spread_len}.{format[1][1]}f}s'
    else:
        spread_str = ' ' * (3 + spread_len + 1)
    mean_len = format[0][0] + 1 + format[0][1]
    return f'{x["center"]:{mean_len}.{format[0][1]}f}s{spread_str}'
