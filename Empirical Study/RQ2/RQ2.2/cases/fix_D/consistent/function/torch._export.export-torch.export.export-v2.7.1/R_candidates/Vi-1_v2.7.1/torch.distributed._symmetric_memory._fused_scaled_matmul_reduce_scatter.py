@torch.library.impl(lib, "fused_scaled_matmul_reduce_scatter", "CUDA")
def _fused_scaled_matmul_reduce_scatter(
    A: torch.Tensor,
    B: torch.Tensor,
    A_scale: torch.Tensor,
    B_scale: torch.Tensor,
    reduce_op: str,
    scatter_dim: int,
    group_name: str,
    bias: Optional[torch.Tensor] = None,
    result_scale: Optional[torch.Tensor] = None,
    out_dtype: Optional[torch.dtype] = None,
    use_fast_accum: bool = False,
) -> torch.Tensor:
    if _is_test_mode:
        return _fused_scaled_matmul_reduce_scatter_fallback(
            A,
            B,
            A_scale,
            B_scale,
            reduce_op,
            scatter_dim,
            group_name,
            bias,
            result_scale,
            out_dtype,
            use_fast_accum,
        )
    with torch.profiler.record_function("fused_matmul_reduce_scatter"):
        return _fused_matmul_reduce_scatter_impl(
            mm_out_op=torch.ops.aten._scaled_mm.out,
            A=A,
            B=B,
            A_scale=A_scale,
            kwargs={
                "scale_b": B_scale,
                "bias": bias,
                "scale_result": result_scale,
                "out_dtype": out_dtype,
                "use_fast_accum": use_fast_accum,
            },
            out_dtype=out_dtype,
            reduce_op=reduce_op,
            scatter_dim=scatter_dim,
            group_name=group_name,
        )
