def _make_mismatch_msg(
    actual: Tensor,
    expected: Tensor,
    diagnostics: Diagnostics,
    *,
    identifier: Optional[Union[str, Callable[[str], str]]] = None,
) -> str:
    scalar_comparison = actual.size() == torch.Size([])
    equality = diagnostics.rtol == 0 and diagnostics.atol == 0

    def append_difference(msg: str, *, type: str, difference: float, index: Tuple[int, ...], tolerance: float) -> str:
        if scalar_comparison:
            msg += f"{type.title()} difference: {difference}"
        else:
            msg += f"Greatest {type} difference: {difference} at index {index}"
        if not equality:
            msg += f" (up to {tolerance} allowed)"
        msg += "\n"
        return msg

    default_identifier = "Scalars" if scalar_comparison else "Tensor-likes"
    if identifier is None:
        identifier = default_identifier
    elif callable(identifier):
        identifier = identifier(default_identifier)

    msg = f"{identifier} are not {'equal' if equality else 'close'}!\n\n"

    if not scalar_comparison:
        msg += (
            f"Mismatched elements: {diagnostics.total_mismatches} / {diagnostics.number_of_elements} "
            f"({diagnostics.total_mismatches / diagnostics.number_of_elements:.1%})\n"
        )

    msg = append_difference(
        msg,
        type="absolute",
        difference=diagnostics.max_abs_diff,
        index=diagnostics.max_abs_diff_idx,
        tolerance=diagnostics.atol,
    )
    msg = append_difference(
        msg,
        type="relative",
        difference=diagnostics.max_rel_diff,
        index=diagnostics.max_rel_diff_idx,
        tolerance=diagnostics.rtol,
    )

    return msg.strip()
