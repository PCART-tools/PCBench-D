def trace_map(proxy_mode, func_overload, f, xs, pos_args):
    leading_dim_size = xs[0].shape[0]

    example_input = _unstack_pytree(xs)[0]
    body_graph = f

    body_graph = reenter_make_fx(body_graph)(*example_input, *pos_args)

    next_name = proxy_mode.tracer.get_fresh_qualname("body_graph_")

    proxy_mode.tracer.root.register_module(next_name, body_graph)

    with disable_proxy_modes_tracing():
        example_outs = body_graph(*example_input, *pos_args)

        def expand_tensor(t):
            if isinstance(t, torch.Tensor):
                return t.expand(leading_dim_size, *t.shape)
            return t

        expanded_outs = pytree.tree_map(expand_tensor, example_outs)

    node_args = (body_graph, list(xs), list(pos_args))
    proxy_args = pytree.tree_map(proxy_mode.tracer.unwrap_proxy, node_args)
    out_proxy = proxy_mode.tracer.create_proxy(
        "call_function", func_overload, proxy_args, {}, name="map_impl"
    )
    return track_tensor_tree(
        expanded_outs, out_proxy, constant=None, tracer=proxy_mode.tracer
    )
