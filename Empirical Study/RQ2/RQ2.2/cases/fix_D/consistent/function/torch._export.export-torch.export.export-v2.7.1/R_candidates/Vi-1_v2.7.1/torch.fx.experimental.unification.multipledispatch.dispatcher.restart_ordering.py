@deprecated(
    "`restart_ordering` is deprecated, if you would like to eagerly order the dispatchers, "
    "you should call the `reorder()` method on each dispatcher.",
    category=FutureWarning,
)
def restart_ordering(on_ambiguity=ambiguity_warn):
    """Deprecated interface to temporarily resume ordering."""
