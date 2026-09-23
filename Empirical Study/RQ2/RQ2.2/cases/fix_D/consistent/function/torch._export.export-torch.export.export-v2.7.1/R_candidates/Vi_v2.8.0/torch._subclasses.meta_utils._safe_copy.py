def _safe_copy(dst: torch.Tensor, src: Optional[torch.Tensor]) -> None:
    if type(src) is not torch.Tensor:
        return
    dst.copy_(src)
