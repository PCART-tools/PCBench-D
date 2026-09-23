def _get_grad_fn_or_grad_acc(t: Union[torch.Tensor, "GradientEdge"]) -> Node:
    if isinstance(t, GradientEdge):
        return t.node
    if t.requires_grad and t.grad_fn is None:
        with torch.enable_grad():
            node = t.view_as(t).grad_fn.next_functions[0][0]  # type: ignore[union-attr]
    else:
        node = t.grad_fn
    assert node is not None
    return node
