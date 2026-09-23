def _is_sym_size_node(node: Node):
    return (
        node.op == "call_function"
        and node.target == torch.ops.aten.sym_size.default
        or node.target == torch.ops.aten.sym_numel.default
        or node.target == torch.ops.aten.sym_numel
        or node.target == torch.ops.aten.sym_size
    )
