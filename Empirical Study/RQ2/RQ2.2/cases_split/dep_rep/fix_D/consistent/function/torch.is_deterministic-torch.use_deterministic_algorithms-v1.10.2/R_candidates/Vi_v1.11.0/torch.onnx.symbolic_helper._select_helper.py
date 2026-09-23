def _select_helper(g, self, dim, index, apply_reshape=True):
    index_const = _maybe_get_scalar(index)
    index_dim = _get_tensor_rank(index)
    if not _is_value(index_const):
        # Index is a constant scalar. Make it a size 1 constant tensor.
        index = g.op("Constant", value_t=torch.LongTensor([index_const]))
    elif index_dim is not None and apply_reshape:
        if index_dim == 0:
            # Index is a scalar. Reshape it to a size 1 tensor.
            index = _reshape_helper(g, index, g.op("Constant", value_t=torch.LongTensor([1])))

    index_scalar_type = index.type().scalarType()
    if index_scalar_type is None or index_scalar_type not in ["Long", "Int"]:
        index = g.op("Cast", index, to_i=cast_pytorch_to_onnx["Long"])
    return g.op("Gather", self, index, axis_i=dim)
