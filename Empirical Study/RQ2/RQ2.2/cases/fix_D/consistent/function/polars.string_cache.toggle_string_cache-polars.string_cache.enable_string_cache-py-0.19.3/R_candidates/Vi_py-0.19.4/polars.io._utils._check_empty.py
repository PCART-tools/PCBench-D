def _check_empty(
    b: BytesIO, *, context: str, raise_if_empty: bool, read_position: int | None = None
) -> BytesIO:
    if raise_if_empty and not b.getbuffer().nbytes:
        hint = (
            f" (buffer position = {read_position}; try seek(0) before reading?)"
            if context in ("StringIO", "BytesIO") and read_position
            else ""
        )
        raise NoDataError(f"empty CSV data from {context}{hint}")
    return b
