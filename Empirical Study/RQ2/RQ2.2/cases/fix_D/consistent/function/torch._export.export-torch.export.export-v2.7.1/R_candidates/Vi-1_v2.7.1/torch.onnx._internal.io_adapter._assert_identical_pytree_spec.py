def _assert_identical_pytree_spec(
    spec1: pytree.TreeSpec, spec2: pytree.TreeSpec, error_message: str
) -> None:
    """Assert the two `TreeSpec` objects are identical.

    Args:
        spec1: The first `TreeSpec` object.
        spec2: The second `TreeSpec` object.
        error_message: The error message to raise if the two `TreeSpec` objects are not
            identical.

    Raises:
        ValueError: If the two `TreeSpec` objects are not identical.
    """
    # TODO(bowbao): Turn this check into diagnostic. Consider warning instead of error.
    pass_if_any_checks: Sequence[Callable[[], bool]] = [
        lambda: spec1 == spec2,
        # FIXME: Bug in `dynamo.export`. Sometimes outputs returned in 'list' instead of 'tuple'.
        lambda: _replace_list_with_tuple(spec1) == _replace_list_with_tuple(spec2),
        # FIXME: Bug in `dynamo.export`. Sometimes single function return is wrapped in list.
        lambda: _open_top_level_sequence_if_single_element(spec1) == spec2,
        lambda: spec1 == _open_top_level_sequence_if_single_element(spec2),
    ]

    if not any(check() for check in pass_if_any_checks):
        raise ValueError(f"{error_message}\nExpect {spec1}.\nActual {spec2}.")
