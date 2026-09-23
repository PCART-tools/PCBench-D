def detach(batch: Batch) -> None:
    """Detaches from autograd graph."""
    for i, x in enumerate(batch):
        batch[i] = x.detach().requires_grad_(x.requires_grad)
