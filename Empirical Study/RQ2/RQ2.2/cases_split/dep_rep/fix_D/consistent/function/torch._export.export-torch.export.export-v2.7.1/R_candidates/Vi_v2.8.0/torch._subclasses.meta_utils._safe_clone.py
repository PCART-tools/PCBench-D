def _safe_clone(src: torch.Tensor) -> Optional[torch.Tensor]:
    if type(src) is not torch.Tensor:
        return None
    return src.clone()
