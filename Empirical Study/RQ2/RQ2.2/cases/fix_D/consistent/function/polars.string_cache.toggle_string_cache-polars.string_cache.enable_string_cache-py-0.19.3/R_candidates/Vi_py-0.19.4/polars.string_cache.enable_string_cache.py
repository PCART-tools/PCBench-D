def enable_string_cache(enable: bool | None = None) -> None:
    """
    Enable the global string cache.

    :class:`Categorical` columns created under the same global string cache have
    the same underlying physical value when string values are equal. This allows the
    columns to be concatenated or used in a join operation, for example.

    Parameters
    ----------
    enable
        Enable or disable the global string cache.

        .. deprecated:: 0.19.3
            ``enable_string_cache`` no longer accepts an argument.
             Call ``enable_string_cache()`` to enable the string cache
             and ``disable_string_cache()`` to disable the string cache.

    See Also
    --------
    StringCache : Context manager for enabling and disabling the string cache.
    disable_string_cache : Function to disable the string cache.

    Notes
    -----
    Enabling the global string cache introduces some overhead.
    The amount of overhead depends on the number of categories in your data.
    It is advised to enable the global string cache only when strictly necessary.

    Consider using the :class:`StringCache` context manager for a more reliable way of
    enabling and disabling the string cache.

    Examples
    --------
    Construct two Series using the same global string cache.

    >>> pl.enable_string_cache()
    >>> s1 = pl.Series("color", ["red", "green", "red"], dtype=pl.Categorical)
    >>> s2 = pl.Series("color", ["blue", "red", "green"], dtype=pl.Categorical)
    >>> pl.disable_string_cache()

    As both Series are constructed under the same global string cache,
    they can be concatenated.

    >>> pl.concat([s1, s2])
    shape: (6,)
    Series: 'color' [cat]
    [
            "red"
            "green"
            "red"
            "blue"
            "red"
            "green"
    ]

    """
    if enable is not None:
        issue_deprecation_warning(
            "`enable_string_cache` no longer accepts an argument."
            " Call `enable_string_cache()` to enable the string cache"
            " and `disable_string_cache()` to disable the string cache.",
            version="0.19.3",
        )
        if enable is False:
            plr.disable_string_cache()
            return

    plr.enable_string_cache()
