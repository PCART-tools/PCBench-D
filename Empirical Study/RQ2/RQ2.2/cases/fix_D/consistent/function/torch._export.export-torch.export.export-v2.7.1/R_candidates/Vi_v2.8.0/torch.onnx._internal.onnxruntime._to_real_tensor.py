def _to_real_tensor(tensor: FakeTensor) -> torch.Tensor:
    if tensor.is_sparse:
        raise ValueError("sparse tensor is not yet supported.")
    out = torch.empty(tensor.size(), dtype=tensor.dtype, device=tensor.device)
    return out
