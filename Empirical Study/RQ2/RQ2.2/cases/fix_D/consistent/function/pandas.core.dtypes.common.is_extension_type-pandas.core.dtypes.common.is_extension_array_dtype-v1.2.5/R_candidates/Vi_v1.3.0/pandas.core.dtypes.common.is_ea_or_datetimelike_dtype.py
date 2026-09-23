def is_ea_or_datetimelike_dtype(dtype: Optional[DtypeObj]) -> bool:
    """
    Check for ExtensionDtype, datetime64 dtype, or timedelta64 dtype.

    Notes
    -----
    Checks only for dtype objects, not dtype-castable strings or types.
    """
    return isinstance(dtype, ExtensionDtype) or (
        isinstance(dtype, np.dtype) and dtype.kind in ["m", "M"]
    )
