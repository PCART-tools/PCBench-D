def _process_null_values(
    null_values: None | str | Sequence[str] | dict[str, str] = None,
) -> None | str | Sequence[str] | list[tuple[str, str]]:
    if isinstance(null_values, dict):
        return list(null_values.items())
    else:
        return null_values
