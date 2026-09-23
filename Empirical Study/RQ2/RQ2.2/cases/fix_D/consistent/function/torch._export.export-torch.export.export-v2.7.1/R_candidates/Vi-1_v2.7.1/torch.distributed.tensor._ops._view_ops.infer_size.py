def infer_size(total_size: int, sizes: Shape) -> Shape:
    """
    One dimension input to view may be "-1".

    Infer the size of this dimension given the total_size.
    """
    infers = [i for i, s in enumerate(sizes) if s == -1]
    size = prod(sizes)
    assert len(infers) <= 1, "can only infer one size"
    if infers:
        size = -size
        missing_size = total_size // size
        assert total_size % size == 0, (
            f"size inferred for -1 is not integral {sizes} should have {total_size} elements."
        )
        return tuple(s if s != -1 else missing_size for s in sizes)
    assert size == total_size, f"sizes do not match {total_size} vs {size}"
    return sizes
