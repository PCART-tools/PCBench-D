def _get_grad_fn_or_grad_acc(t: torch.Tensor) -> Union[Node, None]:
    """
    Get the grad function or grad accumulator for a tensor.

    Accumulate grad nodes are lazily created, so we need to a
    dummy view in order to trigger its creation.
    """
    if t.requires_grad and t.grad_fn is None:
        # if no grad function (leaf tensors) we use view
        viewed_t = t.view_as(t)
        grad_fn = viewed_t.grad_fn
        if grad_fn is not None:
            return grad_fn.next_functions[0][0]
        else:
            raise RuntimeError(
                "Attempted to get grad_fn, but got None."
                "Is this being created in a no-grad context?"
            )
    else:
        return t.grad_fn
