def _get_gradient_divide_factors(
    reduce_scatter_group: dist.ProcessGroup,
    all_reduce_group: Optional[dist.ProcessGroup],
    reduce_dtype: torch.dtype,
    device_type: str = "",
) -> Union[tuple[None, None], tuple[float, float]]:
    # For fp32/bf16, we do not need to worry about overflow/underflow, so we
    # use NCCL's built-in division to avoid separate div kernels
    if reduce_dtype in (torch.float32, torch.bfloat16) and device_type != "mtia":
        return None, None
    data_parallel_size = reduce_scatter_group.size()
    if all_reduce_group is not None:
        data_parallel_size *= all_reduce_group.size()
    # Since fp16 has smaller dynamic range than fp32/bf16, we want to avoid
    # overflow/underflow. For N data parallel workers, each worker computes
    # g_i, and they collectively reduce (g_1 + ... + g_N) / N. To avoid
    # overflow/underflow, we divide by ~sqrt(N) before/after the reduction.
    factor: int = 1
    while data_parallel_size % factor == 0 and data_parallel_size / factor > factor:
        factor *= 2
    factor = float(factor)
    return (factor, data_parallel_size / factor)
