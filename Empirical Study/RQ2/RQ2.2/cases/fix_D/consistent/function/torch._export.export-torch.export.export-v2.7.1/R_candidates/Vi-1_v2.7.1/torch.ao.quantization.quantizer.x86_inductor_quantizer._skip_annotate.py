def _skip_annotate(nodes: list[Node], filter_fn: Optional[FilterFn] = None) -> bool:
    """Determine whether to skip annotation for a list of nodes."""

    # 1) Skip annotate if any node is already annotated
    if _is_any_annotated(nodes):
        return True

    # 2) Proceed annotate if a) a filter function is provided
    # and b) the given nodes list passes the filter function check.
    if filter_fn and filter_fn(nodes):
        return False

    return True
