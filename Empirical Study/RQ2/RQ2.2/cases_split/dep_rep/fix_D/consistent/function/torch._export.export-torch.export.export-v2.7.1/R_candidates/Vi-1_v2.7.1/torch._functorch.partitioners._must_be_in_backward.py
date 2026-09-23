def _must_be_in_backward(node: fx.Node) -> bool:
    return _has_tag_must_be_in_backward(node) or (
        _has_tag_is_backward(node) and is_with_effects(node)
    )
