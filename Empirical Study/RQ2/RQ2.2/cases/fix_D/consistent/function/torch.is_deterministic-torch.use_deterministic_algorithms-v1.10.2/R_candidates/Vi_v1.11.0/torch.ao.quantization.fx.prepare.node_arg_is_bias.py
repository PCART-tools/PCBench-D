def node_arg_is_bias(node: Node, arg: Any) -> bool:
    if not isinstance(node, Node) or node.op != 'call_function' or \
       node.target not in BIAS_INDEX_DICT:
        return False

    for i, node_arg in enumerate(node.args):
        if arg is node_arg and i in \
           BIAS_INDEX_DICT[node.target]:  # type: ignore[index]
            return True

    return node.kwargs.get('bias', None) is arg
