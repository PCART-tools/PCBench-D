def validate_exclusive_idx(rank: int, ex_idx: int):
    """
    Validates that ex_idx is a valid exclusive index
    for the given shape.
    """

    assert isinstance(ex_idx, Dim)
    assert isinstance(rank, Dim)
    assert ex_idx > 0 and ex_idx <= rank
