def _replace_batchnorm(m: torch.fx.GraphModule, train_to_eval: bool):
    """
    Switch batchnorm patterns in the model between train and eval modes.

    Batchnorm has different behavior in train vs eval mode. For exported models,
    however, calling `model.train()` or `model.eval()` does not automatically switch
    the batchnorm behavior between the two modes, so here we need to rewrite the aten
    batchnorm patterns manually to achieve the same effect.
    """
    # TODO(Leslie): This function still fails to support custom momentum and eps value.
    # Enable this support in future updates.

    # Avoid circular dependencies
    from .utils import _get_aten_graph_module_for_pattern

    # Needed to ensure subgraph matches are self-contained
    m.graph.eliminate_dead_code()
    m.recompile()

    def bn_train(
        x: torch.Tensor,
        bn_weight: torch.Tensor,
        bn_bias: torch.Tensor,
        bn_running_mean: torch.Tensor,
        bn_running_var: torch.Tensor,
    ):
        return F.batch_norm(
            x, bn_running_mean, bn_running_var, bn_weight, bn_bias, training=True
        )

    def bn_eval(
        x: torch.Tensor,
        bn_weight: torch.Tensor,
        bn_bias: torch.Tensor,
        bn_running_mean: torch.Tensor,
        bn_running_var: torch.Tensor,
    ):
        return F.batch_norm(
            x, bn_running_mean, bn_running_var, bn_weight, bn_bias, training=False
        )

    example_inputs = (
        torch.randn(1, 1, 3, 3),  # x
        torch.randn(1),  # bn_weight
        torch.randn(1),  # bn_bias
        torch.randn(1),  # bn_running_mean
        torch.randn(1),  # bn_running_var
    )

    device = _assert_and_get_unique_device(m)
    is_cuda = device is not None and device.type == "cuda"
    bn_train_aten = _get_aten_graph_module_for_pattern(
        _WrapperModule(bn_train),
        example_inputs,
        is_cuda,
    )
    bn_eval_aten = _get_aten_graph_module_for_pattern(
        _WrapperModule(bn_eval),
        example_inputs,
        is_cuda,
    )

    if train_to_eval:
        match_pattern = bn_train_aten
        replacement_pattern = bn_eval_aten
    else:
        match_pattern = bn_eval_aten
        replacement_pattern = bn_train_aten

    from torch.fx.subgraph_rewriter import replace_pattern_with_filters

    replace_pattern_with_filters(
        m,
        match_pattern,
        replacement_pattern,
        match_filters=[],
        ignore_literals=True,
    )
    m.recompile()
