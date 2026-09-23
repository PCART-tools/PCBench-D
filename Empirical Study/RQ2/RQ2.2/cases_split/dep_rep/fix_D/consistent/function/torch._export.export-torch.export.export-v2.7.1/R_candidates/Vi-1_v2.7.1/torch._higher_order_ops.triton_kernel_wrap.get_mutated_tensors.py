def get_mutated_tensors(
    kernel_idx: int, constant_args_idx: int, kwargs: dict[str, Any]
) -> list[str]:
    kernel = kernel_side_table.get_kernel(kernel_idx)
    constant_args = kernel_side_table.get_constant_args(constant_args_idx)
    return identify_mutated_tensors(kernel, {**kwargs, **constant_args})
