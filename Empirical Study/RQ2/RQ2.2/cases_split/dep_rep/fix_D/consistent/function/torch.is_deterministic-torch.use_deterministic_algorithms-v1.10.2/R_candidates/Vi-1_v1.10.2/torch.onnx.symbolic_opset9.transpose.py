@parse_args("v", "i", "i")
def transpose(g, self, dim0, dim1):
    if dim0 == dim1:  # micro-optimization
        return self

    # NB: Transpose in ONNX is actually a Permute
    rank = sym_help._get_tensor_rank(self)
    if rank is not None:
        axes = list(range(rank))
        axes[dim0], axes[dim1] = axes[dim1], axes[dim0]
        return g.op("Transpose", self, perm_i=axes)
    else:
        # if we don't have dim information we cannot
        # output a permute so use ATen instead
        if sym_help._operator_export_type == torch.onnx.OperatorExportTypes.ONNX_ATEN_FALLBACK:
            return g.op("ATen", self, operator_s="transpose", dim0_i=dim0, dim1_i=dim1)
        else:
            raise RuntimeError("Unsupported: ONNX export of transpose for tensor "
                               "of unknown rank.")
