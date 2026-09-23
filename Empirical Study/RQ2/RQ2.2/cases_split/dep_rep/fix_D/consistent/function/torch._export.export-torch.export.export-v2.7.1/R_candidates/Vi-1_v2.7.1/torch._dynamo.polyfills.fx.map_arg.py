@substitute_in_graph(_fx_map_arg, can_constant_fold_through=True)
def map_arg(a: Any, fn: Callable[[Node], Any]) -> Any:
    return map_aggregate(a, lambda x: fn(x) if isinstance(x, Node) else x)
