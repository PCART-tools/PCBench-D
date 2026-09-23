def eq_spec(self: pytree.TreeSpec, other: pytree.TreeSpec) -> bool:
    """
    Refinement of TreeSpec.__eq__ where, e.g., torch.Size(...) matches tuple(...).
    See _pytree_subclasses_that_lose_info in proxy_tensor.py for more details.
    """

    def _normalize_type(t):
        return str(_pytree_subclasses_that_lose_info.get(t, t))

    def _match_normalized_structure(a, b):
        if a is b:
            return True
        if _normalize_type(a.type) != _normalize_type(b.type):
            return False
        if a.context != b.context:
            return False
        if len(a.children_specs) != len(b.children_specs):
            return False
        return all(
            _match_normalized_structure(a, b)
            for a, b in zip(a.children_specs, b.children_specs)
        )

    return _match_normalized_structure(self, other)
