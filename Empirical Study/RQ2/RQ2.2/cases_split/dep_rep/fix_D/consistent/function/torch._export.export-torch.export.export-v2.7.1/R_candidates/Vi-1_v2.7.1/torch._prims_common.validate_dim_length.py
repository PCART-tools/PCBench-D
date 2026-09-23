def validate_dim_length(length: int):
    """
    Validates that an object represents a valid
    dimension length.
    """

    if isinstance(length, (int, torch.SymInt)):
        torch._check_is_size(length)
    else:
        # sometimes called with sympy expression by inductor
        assert length >= 0
