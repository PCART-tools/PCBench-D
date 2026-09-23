@_onnx_symbolic("aten::sort")
# TODO(justinchuby): Support multiple quantized args in output
@symbolic_helper.parse_args("v", "i", "i", "none")
def sort(g: jit_utils.GraphContext, self, dim, decending, out=None):
    if out is not None:
        symbolic_helper._unimplemented(
            "Sort", "Out parameter is not supported for sort", self
        )
    self_sizes = symbolic_helper._get_tensor_sizes(self)
    try:
        dim_size = self_sizes[dim]
    except Exception:
        # FIXME(justinchuby): Avoid catching Exception.
        # Catch a more specific exception instead.
        dim_size = None

    if dim_size is None:
        return symbolic_helper._unimplemented("Sort", "input size not accessible", self)

    return g.op("TopK", self, k_i=dim_size, axis_i=dim, outputs=2)
