@parse_args("v", "v", "v", "i")
def where(g, condition, self=None, other=None, _outputs=None):
    # Assumes that torch.where's first argument takes only Bool and Byte tensors.
    if condition.type().scalarType() != "Bool":
        condition = g.op("Cast", condition, to_i=sym_help.cast_pytorch_to_onnx["Bool"])
    if self is None:
        condition = torch.onnx.symbolic_opset9.nonzero(g, condition)
        return sym_help._unbind_helper(g, condition, g.op("Constant", value_t=torch.tensor(1)), _outputs)
    return g.op("Where", condition, self, other)
