def restart_ordering(on_ambiguity=ambiguity_warn):
    """Deprecated interface to temporarily resume ordering.
    """
    warn(
        'restart_ordering is deprecated, if you would like to eagerly order'
        'the dispatchers, you should call the ``reorder()`` method on each'
        ' dispatcher.',
        DeprecationWarning,
    )
