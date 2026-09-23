def is_1d_only_ea_dtype(dtype: DtypeObj | None) -> bool:
    """
    Analogue to is_extension_array_dtype but excluding DatetimeTZDtype.
    """
    # Note: if other EA dtypes are ever held in HybridBlock, exclude those
    #  here too.
    # NB: need to check DatetimeTZDtype and not is_datetime64tz_dtype
    #  to exclude ArrowTimestampUSDtype
    return isinstance(dtype, ExtensionDtype) and not isinstance(
        dtype, (DatetimeTZDtype, PeriodDtype)
    )
