def disable_string_cache() -> bool:
    """
    Disable and clear the global string cache.

    See Also
    --------
    enable_string_cache : Function to enable the string cache.
    StringCache : Context manager for enabling and disabling the string cache.

    Notes
    -----
    Consider using the :class:`StringCache` context manager for a more reliable way of
    enabling and disabling the string cache.

    When used in conjunction with the :class:`StringCache` context manager, the string
    cache will not be disabled until the context manager exits.

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
    return plr.disable_string_cache()
