def _add_disjoint_kwargs(d, **kwargs):
    """
    Update dict *d* with entries in *kwargs*, which must be absent from *d*.
    """
    for k, v in kwargs.items():
        if k in d:
            _api.warn_deprecated(
                "3.3", message=f"The {k!r} parameter to Colorbar has no "
                "effect because it is overridden by the mappable; it is "
                "deprecated since %(since)s and will be removed %(removal)s.")
        d[k] = v
