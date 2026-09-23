def can_create_dicts_with_pyarrow(dtypes: Sequence[PolarsDataType]) -> bool:
    """Check if the given dtypes can be used to create dicts with pyarrow fast path."""
    # TODO: have our own fast-path for dict iteration in Rust
    return (
        _PYARROW_AVAILABLE
        # note: 'ns' precision instantiates values as pandas types - avoid
        and not any(
            (getattr(tp, "time_unit", None) == "ns") for tp in unpack_dtypes(*dtypes)
        )
    )
