def get_expanded_dims(t: torch.Tensor) -> list[int]:
    if not isinstance(t, torch.Tensor):
        return None
    return [i for i in range(t.ndim) if t.stride(i) == 0 and t.size(i) != 1]
