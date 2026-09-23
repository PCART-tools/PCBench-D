def clone_me(x: Optional[torch.Tensor]) -> Optional[torch.Tensor]:
    if x is None:
        return None
    return x.detach().clone().requires_grad_(x.requires_grad)
