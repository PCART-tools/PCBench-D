def _get_per_row_min_max(
        x: torch.Tensor,
        min_vals: torch.Tensor,
        max_vals: torch.Tensor,
        axis: int = 0,
        averaging_const: float = 0.01) -> Tuple[torch.Tensor, torch.Tensor]:
    x_dim = x.size()
    new_axis_list = [i for i in range(len(x_dim))]  # noqa: C416
    new_axis_list[axis] = 0
    new_axis_list[0] = axis
    y = x.permute(*new_axis_list)

    y = torch.flatten(y, start_dim=1)
    # min_vals, max_vals = torch._aminmax(y, 1)
    if math.isinf(min_vals[0]) or math.isinf(max_vals[0]):
        min_vals, max_vals = torch._aminmax(y, 1)
    else:
        min_vals_cur, max_vals_cur = torch._aminmax(y, 1)
        min_vals = min_vals + averaging_const * (min_vals_cur - min_vals)
        max_vals = max_vals + averaging_const * (max_vals_cur - max_vals)
    return min_vals, max_vals
