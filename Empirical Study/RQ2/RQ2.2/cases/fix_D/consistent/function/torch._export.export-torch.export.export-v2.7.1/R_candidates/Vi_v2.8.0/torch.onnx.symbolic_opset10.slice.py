@_onnx_symbolic("aten::slice")
def slice(g: jit_utils.GraphContext, self, *args):
    if len(args) == 4:
        # aten::slice(Tensor self, int dim, int? start=None, int? end=None, int step=1) -> Tensor
        dims, start, end, step = args
    elif len(args) == 3:
        # aten::slice(t[] l, int? start=None, int? end=None, int step=1) -> t[]
        start, end, step = args
        dims = [0]
    else:
        raise errors.SymbolicValueError("Unknown aten::slice signature", self)

    return symbolic_helper._slice_helper(
        g,
        self,
        axes=dims,
        starts=start,
        ends=end,
        steps=step,
    )
