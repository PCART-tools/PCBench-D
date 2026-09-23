def default_tolerances(*inputs: Union[torch.Tensor, torch.dtype]) -> Tuple[float, float]:
    """Returns the default absolute and relative testing tolerances for a set of inputs based on the dtype.

    See :func:`assert_close` for a table of the default tolerance for each dtype.

    Returns:
        (Tuple[float, float]): Loosest tolerances of all input dtypes.
    """
    dtypes = []
    for input in inputs:
        if isinstance(input, torch.Tensor):
            dtypes.append(input.dtype)
        elif isinstance(input, torch.dtype):
            dtypes.append(input)
        else:
            raise TypeError(f"Expected a torch.Tensor or a torch.dtype, but got {type(input)} instead.")
    rtols, atols = zip(*[_DTYPE_PRECISIONS.get(dtype, (0.0, 0.0)) for dtype in dtypes])
    return max(rtols), max(atols)
