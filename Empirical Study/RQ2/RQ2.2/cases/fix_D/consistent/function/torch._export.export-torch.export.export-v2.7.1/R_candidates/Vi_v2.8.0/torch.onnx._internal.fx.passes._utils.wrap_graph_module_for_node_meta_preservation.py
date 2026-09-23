def wrap_graph_module_for_node_meta_preservation(
    graph_module: torch.fx.GraphModule,
) -> Callable:
    """Wrap a GraphModule with contexts to preserve node meta information, such as stacktrace info.

    This is typically useful before calling `make_fx`. Without this wrapper, the
    stacktrace information will be lost afterwards.
    """

    def wrapped(*args):
        with fx_traceback.preserve_node_meta():
            return torch.fx.Interpreter(graph_module).run(*args)

    return wrapped
