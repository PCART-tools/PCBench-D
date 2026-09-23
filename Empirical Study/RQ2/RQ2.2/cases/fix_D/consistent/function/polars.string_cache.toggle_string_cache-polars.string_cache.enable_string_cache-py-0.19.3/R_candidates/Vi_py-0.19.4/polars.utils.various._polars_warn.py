def _polars_warn(msg: str) -> None:
    warnings.warn(
        msg,
        stacklevel=find_stacklevel(),
    )
