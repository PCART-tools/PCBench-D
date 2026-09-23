@_onnx_symbolic("aten::sub")
def sub(g: jit_utils.GraphContext, self, other, alpha=None):
    """
    Consumes sub function and returns the corresponding ONNX operator.

    This function is not meant to be called directly by the user.

    Args:
        g (GraphContext): The graph context.
        self (Tensor): The first operand.
        other (Tensor): The second operand.
        alpha (Optional[Tensor]): A scaling factor to apply to the second operand.
            If `alpha` is not provided, it defaults to 1.

    Returns:
        ONNX operator
    """
    if alpha and symbolic_helper._scalar(symbolic_helper._maybe_get_scalar(alpha)) != 1:
        other = g.op("Mul", other, alpha)
    return g.op("Sub", self, other)
