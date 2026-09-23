def _get_node_type(tree: Any) -> Any:
    if _is_namedtuple_instance(tree):
        return namedtuple
    return type(tree)
