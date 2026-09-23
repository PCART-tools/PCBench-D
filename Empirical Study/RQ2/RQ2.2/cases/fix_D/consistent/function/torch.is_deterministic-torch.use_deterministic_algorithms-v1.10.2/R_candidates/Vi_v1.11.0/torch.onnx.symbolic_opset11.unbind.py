@parse_args("v", "i", "i")
def unbind(g, self, dim=0, _outputs=None):
    if _outputs is None:
        return g.op("SplitToSequence", self, g.op("Constant", value_t=torch.tensor(1, dtype=torch.long)), axis_i=dim, keepdims_i=0)
    else:
        return torch.onnx.symbolic_opset9.unbind(g, self, dim, _outputs)
