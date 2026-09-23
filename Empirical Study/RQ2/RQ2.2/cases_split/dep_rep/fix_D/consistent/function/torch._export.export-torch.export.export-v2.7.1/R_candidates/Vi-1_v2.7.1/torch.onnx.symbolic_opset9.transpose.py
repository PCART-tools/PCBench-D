@_onnx_symbolic("aten::transpose")
@symbolic_helper.quantized_args(True)
@symbolic_helper.parse_args("v", "i", "i")
def transpose(g: jit_utils.GraphContext, self, dim0, dim1):
    if dim0 == dim1:  # micro-optimization
        return self

    # NB: Transpose in ONNX is actually a Permute
    rank = symbolic_helper._get_tensor_rank(self)
    if rank is not None:
        axes = list(range(rank))
        axes[dim0], axes[dim1] = axes[dim1], axes[dim0]
        return g.op("Transpose", self, perm_i=axes)
    else:
        raise errors.SymbolicValueError(
            "Unsupported: ONNX export of transpose for tensor of unknown rank.",
            self,
        )
