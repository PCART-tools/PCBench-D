def _create_operator_type_filter(
    operator_type: Callable,
) -> FilterFn:
    """Create a filter function for a given operator type.

    The filter function takes a list of nodes and returns True if it contains
    exactly one node with the specified operator type, False otherwise.

    For example:
        linear_1: "f32[3, 10]" = torch.ops.aten.linear.default(...) # comes from a module with name `sub.linear1`
        relu: "f32[3, 10]" = torch.ops.aten.relu.default(linear_1); # comes from a module with name `sub.relu1`

    >> operator_type_filter = _create_operator_type_filter(torch.ops.aten.linear.default)
    >> print(operator_type_filter([relu, linear_1]))
    # True  # These two nodes are determined by `_annotate_linear_unary` function and the second node is `linear`.
    """

    def operator_type_filter(nodes: list[Node]):
        num_nodes_with_operator_type = sum(
            node.target == operator_type for node in nodes
        )
        if num_nodes_with_operator_type > 1:
            raise NotImplementedError(
                f"Several nodes within a single pattern are {operator_type}."
            )
        return num_nodes_with_operator_type == 1

    return operator_type_filter
