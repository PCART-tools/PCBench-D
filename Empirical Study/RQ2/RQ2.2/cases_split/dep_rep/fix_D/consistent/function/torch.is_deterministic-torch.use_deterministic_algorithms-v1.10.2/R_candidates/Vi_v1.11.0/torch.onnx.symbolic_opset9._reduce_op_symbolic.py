def _reduce_op_symbolic(onnx_op_name, allow_multi_dim_support=True):
    def symbolic(g, self, dim=None, keepdim=None):
        self = _maybe_cast_reduce_op_input(g, self)
        if dim is None:
            # all-reduce path
            return sym_help._handle_reduce_dim_none(g, self, onnx_op_name)
        else:
            # dim-reduce path
            desc = "is" if allow_multi_dim_support else "i"
            dim, keepdim = sym_help._get_const(dim, desc, "dim"), sym_help._get_const(keepdim, "i", "keepdim")
            dim_list = dim if allow_multi_dim_support else [dim]
            return g.op(onnx_op_name, self, axes_i=dim_list, keepdims_i=keepdim)
    return symbolic
