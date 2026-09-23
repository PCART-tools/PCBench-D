def fuse_matmul_reduce_scatter(reduce_scatter: _ReduceScatterMatch) -> None:
    """
    Fused the pattern

        reduce_scatter_tensor(A @ B, scatter_dim, group_name)

    into

        torch.ops.symm_mem.fused_matmul_reduce_scatter(
            A, B, scatter_dim, group_name,
        )
    """
    if (
        not torch.distributed.is_available()
        or not torch.distributed.is_nccl_available()
    ):
        return

    from torch.distributed._symmetric_memory import (
        is_symm_mem_enabled_for_group,
        restride_A_for_fused_matmul_reduce_scatter,
    )

    input_node, _rs_node, rs_res_node, reduce_op, scatter_dim, group_name = (
        reduce_scatter.input_node,
        reduce_scatter.rs_node,
        reduce_scatter.res_node,
        reduce_scatter.reduce_op,
        reduce_scatter.scatter_dim,
        reduce_scatter.group_name,
    )

    if not is_symm_mem_enabled_for_group(group_name):
        return

    # Currently fused_matmul_reduce_scatter doesn't return the matmul result,
    # so we can't apply the fusion if the matmul result is used by multiple
    # users. This is not a fundamental limitation of the fused op and can be
    # addressed if needed.
    if len(input_node.users) != 1:
        return

    matmul = _find_producer_matmul(input_node)
    if matmul is None:
        return

    if rs_res_node in matmul.arg_ancestor_nodes:
        return

    graph = rs_res_node.graph
    with graph.inserting_before(rs_res_node):
        if "val" in matmul.A_node.meta:
            restrided = restride_A_for_fused_matmul_reduce_scatter(
                _get_tensor(matmul.A_node),
                scatter_dim,
            )
            matmul.A_node = graph.call_function(
                inductor_prims.force_stride_order,
                args=(matmul.A_node, restrided.stride()),
            )

        fused_node = _insert_fused_matmul_reduce_scatter(
            graph,
            matmul,
            reduce_op,
            scatter_dim,
            group_name,
        )
        reduce_scatter.replace_with(fused_node)
        reduce_scatter.erase()
        matmul.erase()

    order = {node: idx for idx, node in enumerate(graph.nodes)}
    nodes_to_raise = sorted(
        matmul.arg_ancestor_nodes,
        key=lambda x: order[x],
    )
    for node in nodes_to_raise:
        if order[node] > order[fused_node]:
            fused_node.prepend(node)
