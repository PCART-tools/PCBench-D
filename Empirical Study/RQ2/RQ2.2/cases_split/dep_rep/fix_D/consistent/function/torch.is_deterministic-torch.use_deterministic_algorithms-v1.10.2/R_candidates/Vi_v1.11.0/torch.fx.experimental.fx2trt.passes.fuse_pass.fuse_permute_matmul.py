def fuse_permute_matmul(gm: torch.fx.GraphModule):
    """
    Fuse pattern like permute + matmul if permute is transposing the last two dimension.
    """
    for node in gm.graph.nodes:
        if node.target == acc_ops.matmul:
            lhs, rhs = node.kwargs["input"], node.kwargs["other"]
            lhs_transposed = rhs_tranposed = False
            skip = False

            if lhs.target == acc_ops.permute and check_permute(lhs):
                lhs_transposed = True
                lhs = lhs.kwargs["input"]

            if rhs.target == acc_ops.permute and check_permute(rhs):
                rhs_tranposed = True
                rhs = rhs.kwargs["input"]

            if (not skip) and (lhs_transposed or rhs_tranposed):
                with gm.graph.inserting_before(node):
                    fused_node = gm.graph.call_function(trt_transposed_matmul, args=(lhs, rhs, lhs_transposed, rhs_tranposed))
                node.replace_all_uses_with(fused_node)

    gm.graph.eliminate_dead_code()
    gm.graph.lint()
    gm.recompile()
    return gm
