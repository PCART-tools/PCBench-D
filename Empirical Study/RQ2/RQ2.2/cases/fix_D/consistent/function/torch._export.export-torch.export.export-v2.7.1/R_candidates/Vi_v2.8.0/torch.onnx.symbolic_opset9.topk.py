@_onnx_symbolic("aten::topk")
# TODO(justinchuby): Support multiple quantized args in output
@symbolic_helper.parse_args("v", "i", "i", "i", "i", "none")
def topk(g: jit_utils.GraphContext, self, k, dim, largest, sorted, out=None):
    if out is not None:
        symbolic_helper._unimplemented(
            "TopK", "Out parameter is not supported for topk", self
        )
    if not largest:
        symbolic_helper._unimplemented("TopK", "Ascending TopK is not supported", self)

    return g.op("TopK", self, k_i=k, axis_i=dim, outputs=2)
