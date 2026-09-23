def parse_percentiles(percentiles: Sequence[float] | float | None) -> Sequence[float]:
    """
    Transforms raw percentiles into our preferred format, adding the 50th percentile.

    Raises a ValueError if the percentile sequence is invalid
    (e.g. outside the range [0, 1])
    """
    if isinstance(percentiles, float):
        percentiles = [percentiles]
    elif percentiles is None:
        percentiles = []
    if not all((0 <= p <= 1) for p in percentiles):
        raise ValueError("percentiles must all be in the range [0, 1]")

    sub_50_percentiles = sorted(p for p in percentiles if p < 0.5)
    at_or_above_50_percentiles = sorted(p for p in percentiles if p >= 0.5)

    if not at_or_above_50_percentiles or at_or_above_50_percentiles[0] != 0.5:
        at_or_above_50_percentiles = [0.5, *at_or_above_50_percentiles]

    return [*sub_50_percentiles, *at_or_above_50_percentiles]
