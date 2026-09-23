def _retrieve_constant(spec: "TreeSpec") -> Any:
    """Given a spec from a pytree registered with register_constant, retrieves the constant"""
    assert _is_constant_holder(spec)
    return tree_unflatten([], spec)
