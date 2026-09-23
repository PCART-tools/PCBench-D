def _replace_dropout(m: torch.fx.GraphModule, train_to_eval: bool):
    """
    Switch dropout patterns in the model between train and eval modes.

    Dropout has different behavior in train vs eval mode. For exported models,
    however, calling `model.train()` or `model.eval()` does not automatically switch
    the dropout behavior between the two modes, so here we need to rewrite the aten
    dropout patterns manually to achieve the same effect.

    See https://github.com/pytorch/pytorch/issues/103681.
    """
    # Avoid circular dependencies
    from .utils import _get_aten_graph_module_for_pattern

    # Needed to ensure subgraph matches are self-contained
    m.graph.eliminate_dead_code()
    m.recompile()

    for inplace in [False, True]:

        def dropout_train(x):
            return F.dropout(x, p=0.5, training=True, inplace=inplace)

        def dropout_eval(x):
            return F.dropout(x, p=0.5, training=False, inplace=inplace)

        example_inputs = (torch.randn(1),)
        if train_to_eval:
            match_pattern = _get_aten_graph_module_for_pattern(
                _WrapperModule(dropout_train),
                example_inputs,
            )
            replacement_pattern = _get_aten_graph_module_for_pattern(
                _WrapperModule(dropout_eval),
                example_inputs,
            )
        else:
            match_pattern = _get_aten_graph_module_for_pattern(
                _WrapperModule(dropout_eval),
                example_inputs,
            )
            replacement_pattern = _get_aten_graph_module_for_pattern(
                _WrapperModule(dropout_train),
                example_inputs,
            )

        from torch.fx.subgraph_rewriter import replace_pattern_with_filters

        replace_pattern_with_filters(
            m,
            match_pattern,
            replacement_pattern,
            match_filters=[],
            ignore_literals=True,
        )
        m.recompile()
