def _insert_fused_matmul_reduce_scatter(
    graph: torch.fx.Graph,
    matmul: _Matmul,
    reduce_op: str,
    scatter_dim: int,
    group_name: str,
) -> torch.fx.Node:
    if type(matmul) == _Matmul:
        return graph.call_function(
            torch.ops.symm_mem.fused_matmul_reduce_scatter.default,
            args=(matmul.A_node, matmul.B_node, reduce_op, scatter_dim, group_name),
        )
    elif type(matmul) == _ScaledMatmul:
        return graph.call_function(
            torch.ops.symm_mem.fused_scaled_matmul_reduce_scatter.default,
            args=(
                matmul.A_node,
                matmul.B_node,
                matmul.A_scale_node,
                matmul.B_scale_node,
                reduce_op,
                scatter_dim,
                group_name,
                matmul.bias_node,
                matmul.result_scale_node,
                matmul.out_dtype,
                matmul.use_fast_accum,
            ),
        )
    else:
        raise AssertionError(f"Unexpected matmul match type: {type(matmul)}")
