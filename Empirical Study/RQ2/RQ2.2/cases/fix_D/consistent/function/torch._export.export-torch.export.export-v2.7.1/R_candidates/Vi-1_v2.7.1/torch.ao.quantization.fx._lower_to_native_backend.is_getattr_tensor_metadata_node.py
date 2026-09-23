def is_getattr_tensor_metadata_node(node):
    return (
        node.op == "call_function"
        and node.target == getattr
        and node.args[1] in ["shape"]
    )
