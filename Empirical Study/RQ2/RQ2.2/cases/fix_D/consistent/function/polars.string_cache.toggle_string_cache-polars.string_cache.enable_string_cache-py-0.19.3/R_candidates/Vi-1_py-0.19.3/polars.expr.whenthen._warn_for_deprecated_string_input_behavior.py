def _warn_for_deprecated_string_input_behavior(input: str) -> None:
    issue_deprecation_warning(
        "in a future version, string input will be parsed as a column name rather than a string literal."
        f" To silence this warning, pass the input as an expression instead: `pl.lit({input!r})`",
        version="0.18.9",
    )
