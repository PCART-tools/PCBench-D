def pad_tensor(tensor: torch.Tensor, pad_dim: int, pad_size: int) -> torch.Tensor:
    if pad_size == 0:
        return tensor
    pad = [0, 0] * (tensor.ndim - pad_dim)
    pad[-1] = pad_size
    return torch.nn.functional.pad(tensor, pad)
