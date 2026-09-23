def decompose_auto_functionalized(graph):
    """Decomposes auto_functionalized nodes into clones and the underlying
    mutation node.

    We assume that the reinplacing pass runs before this; the reinplacing pass
    tells us (via rewriting the arguments or .meta to those nodes) which
    Tensors we should clone and which Tensors are safe to reinplace.
    """
    graph_pass = PatternMatcherPass()

    @register_graph_pattern(
        CallFunctionVarArgs(torch.ops.higher_order.auto_functionalized),
        pass_dict=graph_pass,
    )
    def _(match: Match, *args, **kwargs):
        from torch._higher_order_ops.auto_functionalize import auto_functionalized_dense

        only_clone_these_tensors = tuple(
            match.nodes[0].meta.get("only_clone_these_tensors", [])
        )

        flat_args, spec = pytree.tree_flatten((args, kwargs))

        # NB: we combine (args, kwargs) into flat args for replacing.
        # This is replace_by_example uses make_fx which does not support
        # tracing a function with kwargs.
        def decomp(*flat_args):
            args, kwargs = pytree.tree_unflatten(flat_args, spec)
            assert len(args) == 1
            mode = args[0]
            return auto_functionalized_dense(mode, only_clone_these_tensors, **kwargs)

        match.replace_by_example(decomp, flat_args, run_functional_passes=False)

    @register_graph_pattern(
        CallFunctionVarArgs(torch.ops.higher_order.auto_functionalized_v2),
        pass_dict=graph_pass,
    )
    def _(match: Match, *args, **kwargs):
        from torch._higher_order_ops.auto_functionalize import (
            auto_functionalized_v2_dense,
        )

        only_clone_these_bases = tuple(
            match.nodes[0].meta.get("only_clone_these_tensors", [])
        )

        flat_args, spec = pytree.tree_flatten((args, kwargs))

        def _maybe_resolve_constant_get_attr(node):
            # Resolve getattr node to its value because they don't always have meta["val"]
            if (
                isinstance(node, torch.fx.Node)
                and node.op == "get_attr"
                and "val" not in node.meta
            ):
                const_attr = getattr(graph.owning_module, node.target)  # type: ignore[arg-type]
                assert isinstance(
                    const_attr, (torch.fx.GraphModule, pytree.TreeSpec)
                ), (type(const_attr), const_attr)
                return const_attr
            return node

        flat_args = [_maybe_resolve_constant_get_attr(arg) for arg in flat_args]

        # NB: we combine (args, kwargs) into flat args for replacing.
        # This is replace_by_example uses make_fx which does not support
        # tracing a function with kwargs.
        def decomp(*flat_args):
            args, kwargs = pytree.tree_unflatten(flat_args, spec)
            assert len(args) == 1
            mutable_op = args[0]
            return auto_functionalized_v2_dense(
                mutable_op, only_clone_these_bases, **kwargs
            )

        match.replace_by_example(decomp, flat_args, run_functional_passes=False)

    graph_pass.apply(graph)

    # We need to remove the get_attr registered for _constant_schema and the
    # auto_functioanlized's graph module (it's replaced with original ) when auto_functionalize a hop.
    _to_remove = []
    for node in graph.nodes:
        if node.op == "get_attr" and len(node.users) == 0:
            _to_remove.append(node)
            if hasattr(graph.owning_module, node.target) and isinstance(
                getattr(graph.owning_module, node.target), torch.fx.GraphModule
            ):
                delattr(graph.owning_module, node.target)
    for node in _to_remove:
        graph.erase_node(node)

    graph.lint()

    for _ in graph.find_nodes(
        op="call_function", target=torch.ops.higher_order.auto_functionalized
    ):
        raise AssertionError("auto_functionalized was not removed")

    for _ in graph.find_nodes(
        op="call_function", target=torch.ops.higher_order.auto_functionalized_v2
    ):
        raise AssertionError("auto_functionalized_v2 was not removed")
