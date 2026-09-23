def _is_input_non_float_tensor(node: Node):
    """Check if the input is not a float tensor, so that we can skip quantization for the node
    since observers only works with float Tensors
    """
    if "val" not in node.meta or not isinstance(node.meta["val"], FakeTensor):
        return True
    return node.meta["val"].dtype != torch.float32
