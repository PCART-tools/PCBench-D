@parse_args("v", "i")
def unsqueeze(g, self, dim):
    # Handle negative dim
    if dim < 0:
        rank = sym_help._get_tensor_rank(self)
        if rank is not None:
            warnings.warn("ONNX export unsqueeze with negative axis " + str(dim) +
                          " might cause the onnx model to be incorrect. " +
                          "Negative axis is not supported in ONNX. " +
                          "Axis is converted to " + str(dim + rank + 1) +
                          " based on input shape at export time. " +
                          "Passing an tensor of different rank in execution will be incorrect.")
            dim = dim + rank + 1
        else:
            return _unimplemented("unsqueeze", "negative axis with unknown input rank")

    return sym_help._unsqueeze_helper(g, self, axes_i=[dim])
