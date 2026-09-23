def _scalar(x: Any) -> Number | None:
    """Convert a scalar tensor into a Python value."""
    if isinstance(x, torch.Tensor) and x.shape == ():
        return x.item()
    return None
