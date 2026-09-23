def squeeze(g, self, dim=None):
    if dim is None:
        return g.op("Squeeze", self)

    dim = sym_help._get_const(dim, "i", "dim")

    input_rank = sym_help._get_tensor_rank(self)
    adjusted_dim = dim
    if input_rank is not None and dim < 0:
        adjusted_dim += input_rank
    dim_size = sym_help._get_tensor_dim_size(self, adjusted_dim)
    if (dim < 0 and input_rank is None) or dim_size is None:
        # If onnx shape inference is not on, export always as dynamic.
        # Because we cannot tell if observed static shape is also static at runtime.
        # create "cond" node (condition is shape[i]==1)
        dim_constant = g.op("Constant", value_t=torch.tensor([dim]))
        size = sym_help._size_helper(g, self, dim_constant)
        const_one = g.op("Constant", value_t=torch.ones(1, dtype=torch.int64))
        cond = g.op("Equal", size, const_one)
        # create the "If" node and add the "then" and "else" blocks to it.
        if_node_outputs = g.op("If", cond)
        if_node = if_node_outputs.node()
        if_block = torch.onnx.utils._add_block(if_node)
        squeeze_ = sym_help._squeeze_helper(if_block, self, [dim])
        torch.onnx.utils._add_output_to_block(if_block, squeeze_)
        else_block = torch.onnx.utils._add_block(if_node)
        identity_ = else_block.op("Identity", self)
        torch.onnx.utils._add_output_to_block(else_block, identity_)
        return if_node_outputs

    # For static input shape
    dim = adjusted_dim
    if dim_size > 1:
        warnings.warn("This model contains a squeeze operation on dimension " + str(dim) + ". The size of " +
                      "this dimension in the given input is " + str(dim_size) + ". The model will " +
                      "be exported without the squeeze node. If the model is intended to be used with dynamic " +
                      "input shapes, please export with dynamic_axes argument.")
        return self
    return sym_help._squeeze_helper(g, self, [dim])
