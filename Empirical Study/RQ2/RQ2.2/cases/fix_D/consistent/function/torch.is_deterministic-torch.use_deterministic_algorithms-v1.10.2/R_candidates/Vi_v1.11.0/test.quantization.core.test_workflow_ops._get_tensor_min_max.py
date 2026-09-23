def _get_tensor_min_max(
        X: torch.Tensor,
        running_min: float = float("inf"),
        running_max: float = float("-inf"),
        averaging_const: float = 0.01) -> Tuple[float, float]:
    min_val = X.min().to(dtype=torch.float32).item()
    max_val = X.max().to(dtype=torch.float32).item()

    if not math.isinf(running_min):
        min_val = running_min + averaging_const * (min_val - running_min)
    if not math.isinf(running_max):
        max_val = running_max + averaging_const * (max_val - running_max)

    return min_val, max_val
