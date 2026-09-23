def _loss_fn(
    loss: Callable[[torch.Tensor, torch.Tensor], torch.Tensor], x: object, y: object
) -> object:
    """The returned loss will have the same structure as `x` and `y`, e.g.
    if both are Tensor, we'll return a Tensor
    if both are list, we'll return a list of Tensors
    if both are dict, we'll return a dict with the same key, and value being the loss between the
    two Tensors
    """
    if isinstance(x, torch.Tensor) and isinstance(y, torch.Tensor):
        return loss(x.to(torch.float32), y.to(torch.float32))
    elif isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)):
        return type(x)([_loss_fn(loss, e1, e2) for e1, e2 in zip(x, y)])
    elif isinstance(x, dict) and isinstance(y, dict):
        return {k: _loss_fn(loss, e, y[k]) for k, e in x.items()}
    else:
        return None
