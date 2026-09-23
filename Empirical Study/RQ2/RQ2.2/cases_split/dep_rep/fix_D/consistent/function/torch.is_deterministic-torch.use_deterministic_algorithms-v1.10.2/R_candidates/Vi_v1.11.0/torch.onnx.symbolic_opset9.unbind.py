@parse_args("v", "i", "i")
def unbind(g, self, dim=0, _outputs=None):
    if _outputs is None:
        return sym_help._onnx_opset_unsupported_detailed("unbind", 9, 11, "Dynamic number of outputs not supported")

    outputs = g.op("Split", self, split_i=[1] * _outputs, axis_i=dim, outputs=_outputs)
    outputs = [outputs] if _outputs == 1 else outputs
    squeezed_outputs = [sym_help._squeeze_helper(g, out, [dim]) for out in outputs]
    return squeezed_outputs
