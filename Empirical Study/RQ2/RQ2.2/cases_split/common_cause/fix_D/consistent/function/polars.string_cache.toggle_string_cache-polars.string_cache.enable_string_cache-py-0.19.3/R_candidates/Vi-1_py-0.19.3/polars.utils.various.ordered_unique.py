def ordered_unique(values: Sequence[Any]) -> list[Any]:
    """Return unique list of sequence values, maintaining their order of appearance."""
    seen: set[Any] = set()
    add_ = seen.add
    return [v for v in values if not (v in seen or add_(v))]
