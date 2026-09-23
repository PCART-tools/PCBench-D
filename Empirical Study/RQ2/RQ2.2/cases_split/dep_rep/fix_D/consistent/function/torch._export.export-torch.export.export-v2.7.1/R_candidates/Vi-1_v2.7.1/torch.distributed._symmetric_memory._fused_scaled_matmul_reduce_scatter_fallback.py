@torch.library.impl(lib, "fused_scaled_matmul_reduce_scatter", "Meta")
def _fused_scaled_matmul_reduce_scatter_fallback(
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
    if A_scale.numel() > 1:
        if A_scale.shape[:-1] != A.shape[:-1]:
            raise ValueError(
                "For row-wise scaling, the leading dims of A_scale "
                "must match the leading dims of A "
                f"(A shape: {A.shape}, A_scale shape: {A_scale.shape})"
            )
        A_scale = A_scale.flatten(0, -2).contiguous()
    elif A_scale.numel() != 1:
        raise ValueError(
            "Invalid A_scale shape "
            f"(A shape: {A.shape}, A_scale shape: {A_scale.shape})"
        )

    C = torch._scaled_mm(
        A.flatten(0, -2).contiguous(),
        B,
        A_scale,
        B_scale,
        bias,
        result_scale,
        out_dtype,
        use_fast_accum,
    )
    C = C.view(*A.shape[:-1], B.shape[1])
    res = funcol.reduce_scatter_tensor(
        C,
        reduce_op,
        scatter_dim,
        group_name,
    )
    res = funcol.wait_tensor(res)
    return res
