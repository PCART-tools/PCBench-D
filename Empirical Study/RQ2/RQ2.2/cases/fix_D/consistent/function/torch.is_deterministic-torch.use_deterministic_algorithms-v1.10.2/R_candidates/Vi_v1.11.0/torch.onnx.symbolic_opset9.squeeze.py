def squeeze(g, self, dim=None):
    if dim is None:
        return g.op("Squeeze", self)

    squeeze_dim = sym_help._get_const(dim, "i", "dim")
    # Handle negative dims
    if squeeze_dim < 0:
        rank = sym_help._get_tensor_rank(self)
        if rank is not None:
            warnings.warn("ONNX export squeeze with negative axis " + str(squeeze_dim) +
                          " might cause the onnx model to be incorrect. " +
                          "Negative axis is not supported in ONNX. " +
                          "Axis is converted to " + str(squeeze_dim + rank) +
                          " based on input shape at export time. " +
                          "Passing an tensor of different rank in execution will be incorrect.")
            squeeze_dim += rank
        else:
            return _unimplemented("squeeze", "negative axis with unknown input rank")

    dim_size = sym_help._get_tensor_dim_size(self, squeeze_dim)
    if dim_size is None:
        warnings.warn("This model contains a squeeze operation on dimension " + str(squeeze_dim) + " on an input " +
                      "with unknown shape. Note that if the size of dimension " + str(squeeze_dim) + " of the input " +
                      "is not 1, the ONNX model will return an error. Opset version 11 supports squeezing on " +
                      "non-singleton dimensions, it is recommended to export this model using opset " +
                      "version 11 or higher.")
        return sym_help._squeeze_helper(g, self, axes_i=[squeeze_dim])
    if dim_size > 1:
        warnings.warn("This model contains a squeeze operation on dimension " + str(squeeze_dim) + ". The size of " +
                      "this dimension in the given input is " + str(dim_size) + ". The model will " +
                      "be exported without the squeeze node. If the model is intended to be used with dynamic " +
                      "input shapes, please use opset version 11 to " +
                      "export the model.")
        return self

    warnings.warn("This model contains a squeeze operation on dimension " + str(squeeze_dim) + ". If the model is " +
                  "intended to be used with dynamic input shapes, please use opset version 11 to export the model.")
    return sym_help._squeeze_helper(g, self, axes_i=[squeeze_dim])
