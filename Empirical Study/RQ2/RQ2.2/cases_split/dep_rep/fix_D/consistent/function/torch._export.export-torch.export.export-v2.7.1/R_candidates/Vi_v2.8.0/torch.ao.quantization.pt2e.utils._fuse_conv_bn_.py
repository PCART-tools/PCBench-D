def _fuse_conv_bn_(m: GraphModule) -> None:
    has_bn = any(_is_bn_node(n) for n in m.graph.nodes)
    if not has_bn:
        return
    for n in m.graph.nodes:
        if n.op != "call_function" or n.target not in (
            torch.ops.aten._native_batch_norm_legit_no_training.default,
            torch.ops.aten.batch_norm.default,
        ):
            continue
        bn_node = n
        n = bn_node.args[0]
        if not _is_conv_or_conv_transpose_node(n):
            continue
        conv_node = n
        conv_weight_node = conv_node.args[1]
        conv_bias_node = conv_node.args[2] if len(conv_node.args) > 2 else None
        fold_bn_weights_into_conv_node(
            conv_node, conv_weight_node, conv_bias_node, bn_node, m
        )

    m.graph.eliminate_dead_code()
    m.recompile()
