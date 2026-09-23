def validate_idx(rank: int, idx: int):
    """
    Validates that idx is a valid index for the given shape.
    Assumes the index is already canonicalized.
    """

    assert isinstance(idx, Dim)
    assert isinstance(rank, Dim)

    assert idx >= 0 and idx < rank or idx == 0
