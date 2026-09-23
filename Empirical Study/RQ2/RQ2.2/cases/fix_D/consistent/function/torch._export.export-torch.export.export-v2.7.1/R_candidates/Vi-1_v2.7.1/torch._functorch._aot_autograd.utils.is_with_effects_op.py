def is_with_effects_op(node, op):
    return is_with_effects(node) and node.args[1] == op
