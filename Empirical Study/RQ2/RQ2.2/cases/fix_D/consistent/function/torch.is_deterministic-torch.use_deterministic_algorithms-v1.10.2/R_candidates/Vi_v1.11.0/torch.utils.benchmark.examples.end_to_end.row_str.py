def row_str(rel_diff, diff_seconds, measurement):
    params = measurement.metadata["params"]
    tensor_parameters = measurement.metadata["tensor_parameters"]

    dim = params["dim"]
    x_numel = tensor_parameters["x"]["numel"]
    steps = [params[f"x_step_{i}"] for i in range(dim)]
    order = tensor_parameters['x']["order"]
    order = str("" if all(i == j for i, j in zip(order, range(dim))) else order)

    task_specific = ""
    if measurement.stmt.startswith("torch.topk"):
        dim_str, k_str = measurement.stmt[:-1].replace("torch.topk(x, ", "").split(", ")
        task_specific = f"{dim_str}, {k_str:<8}"
    elif measurement.stmt.startswith("torch.std"):
        pass
    elif measurement.stmt.startswith("torch.sort"):
        task_specific = measurement.stmt[:-1].replace("torch.sort(x, ", "")

    return (
        f"{rel_diff * 100:>5.0f}%     {abs(diff_seconds) * 1e6:>11.1f} us{'':>6}|"
        f"{x_numel:>12}   {params['dtype_str']:>10}   "
        f"{str([params[f'k{i}'] for i in range(dim)]):>17}  "
        f"{str(steps) if not all(i == 1 for i in steps) else '':>12}  {order:>12}"
        f"{'':>8}{task_specific}"
    )
