def rolling_chunk(func, part1, part2, window, *args):
    if part1.shape[0] < window - 1:
        raise NotImplementedError("Window larger than partition size")
    if window > 1:
        extra = window - 1
        combined = pd.concat([part1.iloc[-extra:], part2])
        applied = func(combined, window, *args)
        return applied.iloc[extra:]
    else:
        return func(part2, window, *args)
