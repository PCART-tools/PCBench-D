def _reduce_with_dtype(onnx_op, name):
    symbolic = _reduce_op_symbolic(onnx_op)

    @overload_by_arg_count
    def reduce(g, *args, **kwargs):
        @parse_args("v", "none")
        def reduce_nodim(g, self, dtype):
            if dtype.node().kind() != "prim::Constant":
                return _unimplemented(name, "dtype")
            return symbolic(g, self)

        @parse_args("v", "v", "i", "none")
        def reduce_dim(g, self, dim, keepdim, dtype):
            if dtype.node().kind() != "prim::Constant":
                return _unimplemented(name, "dtype")
            return symbolic(g, self, dim, keepdim)
        return reduce_nodim, reduce_dim
    return reduce
