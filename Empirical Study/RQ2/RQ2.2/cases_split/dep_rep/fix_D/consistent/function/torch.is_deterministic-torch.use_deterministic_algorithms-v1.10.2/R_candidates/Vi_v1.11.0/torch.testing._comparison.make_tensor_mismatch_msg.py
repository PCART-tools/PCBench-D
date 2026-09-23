def make_tensor_mismatch_msg(
    actual: torch.Tensor,
    expected: torch.Tensor,
    mismatches: torch.Tensor,
    *,
    rtol: float,
    atol: float,
    identifier: Optional[Union[str, Callable[[str], str]]] = None,
):
    """Makes a mismatch error message for tensors.

    Args:
        actual (torch.Tensor): Actual tensor.
        expected (torch.Tensor): Expected tensor.
        mismatches (torch.Tensor): Boolean mask of the same shape as ``actual`` and ``expected`` that indicates the
            location of mismatches.
        rtol (float): Relative tolerance.
        atol (float): Absolute tolerance.
        identifier (Optional[Union[str, Callable[[str], str]]]): Optional description for the tensors. Can be passed
            as callable in which case it will be called by the default value to create the description at runtime.
            Defaults to "Tensor-likes".
    """
    number_of_elements = mismatches.numel()
    total_mismatches = torch.sum(mismatches).item()
    extra = (
        f"Mismatched elements: {total_mismatches} / {number_of_elements} "
        f"({total_mismatches / number_of_elements:.1%})"
    )

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
    return _make_mismatch_msg(
        default_identifier="Tensor-likes",
        identifier=identifier,
        extra=extra,
        abs_diff=max_abs_diff.item(),
        abs_diff_idx=_unravel_index(max_abs_diff_flat_idx.item(), mismatches.shape),
        atol=atol,
        rel_diff=max_rel_diff.item(),
        rel_diff_idx=_unravel_index(max_rel_diff_flat_idx.item(), mismatches.shape),
        rtol=rtol,
    )
