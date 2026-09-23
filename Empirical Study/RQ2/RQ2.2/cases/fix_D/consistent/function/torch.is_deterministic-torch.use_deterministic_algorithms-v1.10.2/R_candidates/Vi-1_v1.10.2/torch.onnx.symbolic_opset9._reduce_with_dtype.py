def _reduce_with_dtype(onnx_op, name, allow_multi_dim_support=True):
    symbolic = _reduce_op_symbolic(onnx_op, allow_multi_dim_support=allow_multi_dim_support)

    @overload_by_arg_count
    def reduce(g, *args, **kwargs):
        @parse_args("v", "none")
        def reduce_nodim(g, self, dtype):
            if dtype.node().kind() != "prim::Constant":
                return _unimplemented(name, "dtype")
            return symbolic(g, self)

        dim_desc = "is" if allow_multi_dim_support else "i"

        @parse_args("v", dim_desc, "i", "none")
        def reduce_dim(g, self, dim, keepdim, dtype):
            if dtype.node().kind() != "prim::Constant":
                return _unimplemented(name, "dtype")
            return symbolic(g, self, dim, keepdim)
        return reduce_nodim, reduce_dim
    return reduce
