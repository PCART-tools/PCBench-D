def _trace_mismatches(actual: Tensor, expected: Tensor, mismatches: Tensor, *, rtol: float, atol: float) -> Diagnostics:
    """Traces mismatches and returns diagnostic information.

    Args:
        actual (Tensor): Actual tensor.
        expected (Tensor): Expected tensor.
        mismatches (Tensor): Boolean mask of the same shape as :attr:`actual` and :attr:`expected` that indicates
            the location of mismatches.

    Returns:
        (Diagnostics): Mismatch diagnostics with the following attributes:

            - ``number_of_elements`` (int): Number of elements in each tensor being compared.
            - ``total_mismatches`` (int): Total number of mismatches.
            - ``max_abs_diff`` (Union[int, float]): Greatest absolute difference of the inputs.
            - ``max_abs_diff_idx`` (Union[int, Tuple[int, ...]]): Index of greatest absolute difference.
            - ``atol`` (float): Allowed absolute tolerance.
            - ``max_rel_diff`` (Union[int, float]): Greatest relative difference of the inputs.
            - ``max_rel_diff_idx`` (Union[int, Tuple[int, ...]]): Index of greatest relative difference.
            - ``rtol`` (float): Allowed relative tolerance.

            For ``max_abs_diff`` and ``max_rel_diff`` the type depends on the :attr:`~torch.Tensor.dtype` of the inputs.
    """
    number_of_elements = mismatches.numel()
    total_mismatches = torch.sum(mismatches).item()

    a_flat = actual.flatten()
    b_flat = expected.flatten()
    matches_flat = ~mismatches.flatten()

    abs_diff = torch.abs(a_flat - b_flat)
    # Ensure that only mismatches are used for the max_abs_diff computation
    abs_diff[matches_flat] = 0
    max_abs_diff, max_abs_diff_flat_idx = torch.max(abs_diff, 0)

    rel_diff = abs_diff / torch.abs(b_flat)
    # Ensure that only mismatches are used for the max_rel_diff computation
    rel_diff[matches_flat] = 0
    max_rel_diff, max_rel_diff_flat_idx = torch.max(rel_diff, 0)

    return Diagnostics(
        number_of_elements=number_of_elements,
        total_mismatches=cast(int, total_mismatches),
        max_abs_diff=max_abs_diff.item(),
        max_abs_diff_idx=_unravel_index(max_abs_diff_flat_idx.item(), mismatches.shape),
        atol=atol,
        max_rel_diff=max_rel_diff.item(),
        max_rel_diff_idx=_unravel_index(max_rel_diff_flat_idx.item(), mismatches.shape),
        rtol=rtol,
    )
