def _check_empty(b: BytesIO, context: str, read_position: int | None = None) -> BytesIO:
    if not b.getbuffer().nbytes:
        hint = (
            f" (buffer position = {read_position}; try seek(0) before reading?)"
            if context in ("StringIO", "BytesIO") and read_position
            else ""
        )
        raise NoDataError(f"empty CSV data from {context}{hint}")
    return b
