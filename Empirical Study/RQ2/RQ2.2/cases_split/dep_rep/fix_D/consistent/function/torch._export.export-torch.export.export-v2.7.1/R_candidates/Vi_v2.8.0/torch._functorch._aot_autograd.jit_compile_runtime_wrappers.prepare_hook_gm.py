def prepare_hook_gm(aot_config, fn, args):
    from torch._functorch._aot_autograd.dispatch_and_compile_graph import _create_graph

    fn, args = create_wrap_fn(fn, args)
    gm = _create_graph(fn, args, aot_config=aot_config)
    return gm
