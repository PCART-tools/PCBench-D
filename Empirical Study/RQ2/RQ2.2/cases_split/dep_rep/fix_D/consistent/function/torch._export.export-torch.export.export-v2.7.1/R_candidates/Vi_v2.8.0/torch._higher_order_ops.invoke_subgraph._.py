@invoke_subgraph.py_impl(ProxyTorchDispatchMode)
def _(proxy_mode: ProxyTorchDispatchMode, subgraph, identifier, *operands):
    # Check if we have already traced the subgraph.
    graph = None
    invoke_subgraph_cache = get_invoke_subgraph_cache()
    if invoke_subgraph_cache:
        graph = invoke_subgraph_cache.get_proxy_dispatch_entry(identifier)

    if graph is None:
        from torch._dynamo.utils import dynamo_timed

        with dynamo_timed("invoke_subgraph_proxy_tensor", log_pt2_compile_event=True):
            graph = reenter_make_fx(subgraph)(*operands)

        from torch._guards import detect_fake_mode

        fake_mode = detect_fake_mode(operands)
        insert_deferred_runtime_asserts(
            graph,
            fake_mode.shape_env,
            "invoke_subgraph_proxy_torch_dispatch_mode",
            export=True,
        )
        graph.recompile()

        assert isinstance(proxy_mode.tracer, torch.fx.Tracer)
        if invoke_subgraph_cache:
            invoke_subgraph_cache.add_proxy_dispatch_entry(identifier, graph)

    node_args = (graph, identifier, *operands)

    def _unwrap_proxy(arg):
        if isinstance(arg, torch.fx.GraphModule):
            # NOTE: [invoke_subgraph proxy_mode x auto_functionalize]
            # Previously, we assumed that `invoke_subgraph` would always be traced with the same tracer.
            # This allowed us to cache modules by their identifiers, assuming they were already registered.
            #
            # However, this assumption no longer holds when we auto-functionalize `invoke_subgraph`.
            # auto_functionalize functionalizes the subgraph and wrap it with `FunctionWithNoFreeVars`.
            # In the proxy mode implementation of `auto_functionalized_v2`, we need to materialize `FunctionWithNoFreeVars`
            # input as a graph module. To do this, we re-trace the `invoke_subgraph` hop, which starts a new sub-tracer
            # (see NOTE [materialize callable inputs as graph]). # When the new sub-tracer traces the `invoke_subgraph`
            # with a previously cached identifier, the corresponding graph module might not
            # exist as a submodule in the new tracer's root. Therefore, we register it as a submodule below.
            #
            # The alternative is to give a new identifer when we re-trace the invoke_subgraph but this will increase
            # the compilatoin time, which defeats the purpose of caching.
            registered_before = False
            for (
                _,
                submod,
            ) in proxy_mode.tracer.root.named_modules():  # type: ignore[union-attr]
                if arg is submod:
                    registered_before = True

            if not registered_before:
                qualname = proxy_mode.tracer.get_fresh_qualname("repeated_subgraph")  # type: ignore[union-attr]
                proxy_mode.tracer.root.register_module(qualname, arg)  # type: ignore[union-attr]
        return proxy_mode.tracer.unwrap_proxy(arg)  # type: ignore[union-attr]

    proxy_args = pytree.tree_map(_unwrap_proxy, node_args)  # type: ignore[union-attr]
    out_proxy = proxy_mode.tracer.create_proxy(
        "call_function", invoke_subgraph, proxy_args, {}
    )

    example_out = invoke_subgraph(graph, identifier, *operands)
    return track_tensor_tree(
        example_out, out_proxy, constant=None, tracer=proxy_mode.tracer
    )
