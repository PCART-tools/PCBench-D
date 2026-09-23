def raise_ioerror(error):
    warnings.warn(
        "raise_ioerror is deprecated and will be removed in a future release. "
        "Use raise_oserror instead.",
        DeprecationWarning,
    )
    return raise_oserror(error)
