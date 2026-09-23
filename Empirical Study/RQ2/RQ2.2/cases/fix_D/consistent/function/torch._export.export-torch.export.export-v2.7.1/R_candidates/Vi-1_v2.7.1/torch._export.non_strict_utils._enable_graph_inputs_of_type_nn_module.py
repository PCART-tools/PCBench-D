@contextlib.contextmanager
def _enable_graph_inputs_of_type_nn_module(
    args: Optional[tuple[tuple[Any], dict[Any, Any]]],
):
    if args is None:
        yield
        return

    module_types = _get_graph_inputs_of_type_nn_module(args)
    _enter_enable_graph_inputs_of_type_nn_module(module_types)
    try:
        yield
    finally:
        _exit_enable_graph_inputs_of_type_nn_module(module_types)
