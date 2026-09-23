@compatibility(is_backward_compatible=False)
def get_node_target(submodules: Dict[str, torch.nn.Module], node: torch.fx.Node) -> str:
    """
    Given a `node` returns its target typename.

    For "call_method" node, return node.target which is the name of that method being called.
    This could potential lead to conflict but should be okay because normally it's on a tensor.

    For "call_function" node, return typename of node.target.

    For "call_module" node, return typename of the module that node.target point to.

    If seeing "_VariableFunctionsClass" in the target name string, it will be replaced by
    "torch". e.g. _VariableFunctionsClass.relu would become torch.relu.
    """

    assert node.op in CALLABLE_NODE_OPS, (
        "Expect op types of " + ", ".join(CALLABLE_NODE_OPS) + f", but found {node.op}"
    )

    if node.op == "call_module":
        assert isinstance(node.target, str)
        return torch.typename(submodules[node.target])
    elif node.op == "call_function":
        target: Any = node.target
        return (
            f"acc_ops.{target.__name__}"
            if target.__module__ is not None and "acc_ops" in target.__module__
            else _get_qualified_name(target)
        )
    else:
        assert isinstance(node.target, str)
        return node.target
