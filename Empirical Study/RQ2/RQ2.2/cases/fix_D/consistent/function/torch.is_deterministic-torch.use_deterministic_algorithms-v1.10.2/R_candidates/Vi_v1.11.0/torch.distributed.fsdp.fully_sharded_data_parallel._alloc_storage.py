@torch.no_grad()
def _alloc_storage(data: torch.Tensor, size: torch.Size) -> None:
    """Allocate storage for a tensor."""
    if data.storage().size() == size.numel():  # no need to reallocate
        return
    assert (
        data.storage().size() == 0
    ), "Then tensor storage should have been resized to be 0."
    data.storage().resize_(size.numel())  # type: ignore[attr-defined]
