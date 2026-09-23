def _is_bn_node(n: Node):
    return (
        _is_supported_batch_norm_for_training(n)
        or n.target == torch.ops.aten._native_batch_norm_legit_no_training.default
    )
