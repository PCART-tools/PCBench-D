def _prepare_alpha(
    com: float | int | None = None,
    span: float | int | None = None,
    half_life: float | int | None = None,
    alpha: float | int | None = None,
) -> float:
    """Normalise EWM decay specification in terms of smoothing factor 'alpha'."""
    if sum((param is not None) for param in (com, span, half_life, alpha)) > 1:
        raise ValueError(
            "parameters 'com', 'span', 'half_life', and 'alpha' are mutually exclusive"
        )
    if com is not None:
        if com < 0.0:
            raise ValueError(f"require 'com' >= 0 (found {com!r})")
        alpha = 1.0 / (1.0 + com)

    elif span is not None:
        if span < 1.0:
            raise ValueError(f"require 'span' >= 1 (found {span!r})")
        alpha = 2.0 / (span + 1.0)

    elif half_life is not None:
        if half_life <= 0.0:
            raise ValueError(f"require 'half_life' > 0 (found {half_life!r})")
        alpha = 1.0 - math.exp(-math.log(2.0) / half_life)

    elif alpha is None:
        raise ValueError("one of 'com', 'span', 'half_life', or 'alpha' must be set")

    elif not (0 < alpha <= 1):
        raise ValueError(f"require 0 < 'alpha' <= 1 (found {alpha!r})")

    return alpha
