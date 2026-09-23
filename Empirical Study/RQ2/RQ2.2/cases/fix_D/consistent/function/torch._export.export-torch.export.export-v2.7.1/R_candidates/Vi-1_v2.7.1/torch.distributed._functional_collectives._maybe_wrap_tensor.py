def _maybe_wrap_tensor(self) -> torch.Tensor:
    if _are_we_tracing():
        return wait_tensor(self)
    res = AsyncCollectiveTensor(self)
    return cast(torch.Tensor, res)
