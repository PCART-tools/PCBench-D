@register_inference_rule(torch.tensor)
def tensor_inference_rule(n: Node, symbols, constraints, counter):
    """
    If the tensor is a scalar, we will skip it since we
    do not support scalars yet. We will add support in the future
    if it's needed. For our examples so far, scalars are not needed.
    """
    return [], counter
