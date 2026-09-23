@run_const_graph.py_functionalize_impl
def run_const_graph_functional(ctx, graph, args):
    unwrapped_args = ctx.unwrap_tensors(args)

    with ctx.redispatch_to_next():
        out = run_const_graph(*unwrapped_args)
        return ctx.wrap_tensors(out)
