def node_bool_tensor_arg_indexes(node: Node) -> List[int]:
    """
    Returns indexes of boolean Tensor args
    """
    if node.op == "call_method" and node.target == "masked_fill":
        return [1]
    return []
