def _scalar(x: torch.Tensor):
    """Convert a scalar tensor into a Python value."""
    assert x.numel() == 1
    return x[0]
