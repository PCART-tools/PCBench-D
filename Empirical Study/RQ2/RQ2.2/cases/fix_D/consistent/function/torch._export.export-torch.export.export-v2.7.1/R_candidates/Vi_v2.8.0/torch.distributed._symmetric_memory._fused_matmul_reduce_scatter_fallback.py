@torch.library.impl(lib, "fused_matmul_reduce_scatter", "Meta")
def _fused_matmul_reduce_scatter_fallback(
    A: torch.Tensor,
    B: torch.Tensor,
    reduce_op: str,
    scatter_dim: int,
    group_name: str,
) -> torch.Tensor:
    res = funcol.reduce_scatter_tensor(A @ B, reduce_op, scatter_dim, group_name)
    res = funcol.wait_tensor(res)
    return res
