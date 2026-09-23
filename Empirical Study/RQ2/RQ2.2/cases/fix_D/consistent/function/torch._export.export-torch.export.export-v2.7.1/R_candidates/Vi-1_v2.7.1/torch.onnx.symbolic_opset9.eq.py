@_onnx_symbolic("aten::eq")
@symbolic_helper.quantized_args(True, True)
def eq(g: jit_utils.GraphContext, self, other):
    if isinstance(self.type(), _C.DeviceObjType) and isinstance(
        other.type(), _C.DeviceObjType
    ):
        # ONNX doesn't have devices, so consider them all to be equal.
        # The no-op check for equality will get constant-folded.
        return g.op("Constant", value_t=torch.tensor(True, dtype=torch.bool))
    self_node = self.node()
    other_node = other.node()
    if self_node.kind() == other_node.kind() == "onnx::Constant":
        if self_node.kindOf("value") == other_node.kindOf("value") == "s":
            # Exporting strings to ONNX is not supported.
            # If both strings are constant, we can compare them directly.
            # The no-op check for equality will get constant-folded.
            return g.op(
                "Constant",
                value_t=torch.tensor(
                    self_node.s("value") == other_node.s("value"),
                    dtype=torch.bool,
                ),
            )

    return g.op("Equal", self, other)
