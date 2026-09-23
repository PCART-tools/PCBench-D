def _create_module_name_filter(module_name: str) -> FilterFn:
    """Create a filter function for a given module name.

    The filter function takes a list of nodes (as determined by the annotate function)
    and return True if *all* nodes come from the specified module name, False otherwise.

    For example:
        linear_1: "f32[3, 10]" = torch.ops.aten.linear.default(...) # comes from a module with name `sub.linear1`
        relu: "f32[3, 10]" = torch.ops.aten.relu.default(linear_1); # comes from a module with name `sub.relu1`

    >> module_name_filter = _create_module_name_filter_inner("sub")
    >> print(module_name_filter([relu, linear_1]))
    # True  # These two nodes are determined by `_annotate_linear_unary` function and from "sub".
    """

    filter_fn = _get_module_name_filter(module_name)

    def check_all_nodes_from_module(nodes: list[Node]) -> bool:
        all_nodes_from_module_name: bool = all(filter_fn(n) for n in nodes)
        return all_nodes_from_module_name

    return check_all_nodes_from_module
