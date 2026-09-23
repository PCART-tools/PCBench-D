def trace(
    mod: nn.Module,
    sample_inputs: List[torch.Tensor],
    remove_assertions: bool = True,
    remove_exceptions: bool = True,
    use_acc_normalization: bool = True,
    ast_rewriter_allow_list: Optional[Set[Type[nn.Module]]] = None,
    leaf_module_list: Optional[Set[Type[nn.Module]]] = None,
) -> torch.fx.GraphModule:
    """
    Performs tracing and arg normalization specialized for accelerator lowering.

    It first rewrites the AST of the module's methods (and all attr methods
    recursively) to transform un-tracable parts of the module to make them
    traceable.

    It then traces to the functional level so that optimizations and backend
    accelerator importers have the ability to see and/or change inputs to each
    op.

    It then removes assertions and exception wrappers found during symbolic
    tracing if requested based on remove_assertions and remove_exceptions

    Dead code is then eliminated, which will e.g. remove any nodes that were
    only used by assertions or exceptions if they were removed.

    It then performs normalization on args/kwargs, aligning any arg that can be
    moved to kwarg to be so, and then making default values explicit.

    Args:

        mod (Module): The module to transform and trace.

        sample_inputs (Tuple[Union[torch.Tensor, List[torch.Tensor]]]):
                Sample inputs with which to run shape prop.

        remove_assertions (bool): Whether to remove assertion nodes from
                                    the graph after symbolic tracing.

        remove_exceptions (bool): Whether to remove exception wrapper nodes
                                    from the graph after symbolic tracing.

        use_acc_normalization (bool): Whether to use acc-specific
                                        normalization to all acc_ops.

        ast_rewriter_allow_list (Optional[Set[nn.Module]]): Optional allow list of
                                            modules that need AST rewriting.

        leaf_module_list (Optional[Set[nn.Module]]): Optional leaf module list where
                                            modules will not be traced into.

    """
    if mod.training:
        warnings.warn(
            "acc_tracer does not support currently support models for training."
            " Calling eval on model before tracing."
        )
        mod.eval()

    # Rewrite the module to make it symbolic traceable, and then trace it.
    rewritten_graph, rewritten_mod = AccRewritingTracer().trace(
        mod,
        ast_rewriter_allow_list=ast_rewriter_allow_list,
        leaf_module_list=leaf_module_list,
    )

    assert isinstance(rewritten_mod, nn.Module)
    # Note: use the rewritten_mod here as the root. This is necessary because
    # RewrittenModule includes a new module for the ConditionalExceptionWrapper.
    traced = torch.fx.GraphModule(rewritten_mod, rewritten_graph)

    # Now remove all assertions and exceptions if requested.
    if remove_assertions:
        _remove_assertions(traced)
    if remove_exceptions:
        _remove_exceptions(traced)

    # Cleanup any dead code from the original module as well as resulting dead
    # nodes after removing assertions and exceptions.
    traced.graph.eliminate_dead_code()

    # Now normalize args/kwargs to make default values visible. Leave args/kwargs as
    # they were, since all-kwarg normalization is broken, and we don't need it anyway.
    shape_prop.ShapeProp(traced).propagate(*sample_inputs)
    traced = NormalizeArgs(traced, normalize_to_only_use_kwargs=False).transform()

    # Normalize to acc-specialized wrappers for consistency across op naming and
    # ensuring all kwarg usage.
    if use_acc_normalization:
        acc_normalizer.normalize(traced)

    traced.recompile()

    return traced
