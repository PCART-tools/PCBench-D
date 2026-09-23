def is_with_effects(node):
    return (
        node.op == "call_function"
        and node.target == torch.ops.higher_order.with_effects
    )
