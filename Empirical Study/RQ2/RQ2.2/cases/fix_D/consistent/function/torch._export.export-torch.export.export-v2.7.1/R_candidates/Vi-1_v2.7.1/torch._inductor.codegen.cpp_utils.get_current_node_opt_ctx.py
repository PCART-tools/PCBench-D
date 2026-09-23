def get_current_node_opt_ctx() -> OptimizationContext:
    assert V.interpreter.current_node
    return get_opt_ctx(V.interpreter.current_node)
