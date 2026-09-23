def _adaptive_pool(name, type, tuple_fn, fn=None):
    def symbolic_fn(g, input, output_size):
        # _adaptive_pool is supported for cases where output_size is 1 for all dimensions,
        # by executing a GlobalPool.
        # It is also supported for cases where the output size is a factor of the input size.
        # For these cases the stride and kernel size are uniform along all the indices of
        # the same dimension, which makes it possible to export it to ONNX.
        # for MaxPool, GlobalMaxPool does not return indices,
        # so we try using max_poolxd_with_indices, and if it is not possible
        # (input is not a complete tensor or output size not factor of input size)
        # then we call GlobalAveragePool and return None for the indices
        try:
            output_size = _parse_arg(output_size, "is")
        except Exception:
            return sym_help._onnx_unsupported("adaptive pooling, since output_size is not constant.")
        if output_size == [1] * len(output_size) and type == "AveragePool":
            return g.op("GlobalAveragePool", input)
        sizes = sym_help._get_tensor_sizes(input)
        try:
            dim = sizes[2:]
        except Exception:
            dim = None
        if dim is None or any([i is None for i in dim]):
            if output_size == [1] * len(output_size):
                return g.op("GlobalMaxPool", input), None
            return _unimplemented(name, "input size not accessible")
        # verify if output size % input size = 0 for all dim
        mod = [dim[i] % output_size[i] for i in range(0, len(dim))]
        if mod != [0] * len(mod):
            if output_size == [1] * len(output_size):
                return g.op("GlobalMaxPool", input), None
            if sym_help._operator_export_type == torch.onnx.OperatorExportTypes.ONNX_ATEN_FALLBACK:
                return _unimplemented(name, "output size that are not factor of input size")
            else:
                return sym_help._onnx_unsupported(name + ", since output size is not factor of input size")
        k = [int(dim[i] / output_size[i]) for i in range(0, len(dim))]
        # call max_poolxd_with_indices to get indices in the output
        if type == "MaxPool":
            return fn(g, input, k, k, (0,) * len(dim), (1,) * len(dim), False)
        output = g.op(type, input,
                      kernel_shape_i=tuple_fn(k),
                      strides_i=tuple_fn(k))
        return output
    return symbolic_fn
