def _get_comparison_dtype(dtype: torch.dtype) -> torch.dtype:
    """Selects the comparison dtype based on the input dtype.

    Returns:
        Highest precision dtype of the same dtype category as the input. :class:`torch.bool` is treated as integral
        dtype.
    """
    if dtype.is_complex:
        return torch.complex128
    elif dtype.is_floating_point:
        return torch.float64
    else:
        return torch.int64
