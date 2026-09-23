def _xl_setup_table_options(
    table_style: dict[str, Any] | str | None
) -> tuple[dict[str, Any] | str | None, dict[str, Any]]:
    """Setup table options, distinguishing style name from other formatting."""
    if isinstance(table_style, dict):
        valid_options = (
            "style",
            "banded_columns",
            "banded_rows",
            "first_column",
            "last_column",
        )
        for key in table_style:
            if key not in valid_options:
                raise ValueError(f"Invalid table style key:{key}")

        table_options = table_style.copy()
        table_style = table_options.pop("style", None)
    else:
        table_options = {}

    return table_style, table_options
