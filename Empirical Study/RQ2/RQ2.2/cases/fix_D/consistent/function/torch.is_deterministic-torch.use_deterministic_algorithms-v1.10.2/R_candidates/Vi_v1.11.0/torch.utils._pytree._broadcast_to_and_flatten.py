def _broadcast_to_and_flatten(pytree: PyTree, spec: TreeSpec) -> Optional[List[Any]]:
    assert isinstance(spec, TreeSpec)

    if _is_leaf(pytree):
        return [pytree] * spec.num_leaves
    if isinstance(spec, LeafSpec):
        return None
    node_type = _get_node_type(pytree)
    if node_type != spec.type:
        return None

    flatten_fn = SUPPORTED_NODES[node_type].flatten_fn
    child_pytrees, ctx = flatten_fn(pytree)

    # Check if the Node is different from the spec
    if len(child_pytrees) != len(spec.children_specs) or ctx != spec.context:
        return None

    # Recursively flatten the children
    result : List[Any] = []
    for child, child_spec in zip(child_pytrees, spec.children_specs):
        flat = _broadcast_to_and_flatten(child, child_spec)
        if flat is not None:
            result += flat
        else:
            return None

    return result
