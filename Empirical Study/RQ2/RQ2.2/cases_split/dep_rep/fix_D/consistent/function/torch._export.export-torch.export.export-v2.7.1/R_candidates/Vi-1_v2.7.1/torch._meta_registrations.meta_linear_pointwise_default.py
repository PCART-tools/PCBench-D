    @register_meta(torch.ops.mkldnn._linear_pointwise.default)
    def meta_linear_pointwise_default(
        input_tensor, weight, bias, attr, scalars, algorithm
    ):
        return input_tensor.new_empty((*input_tensor.shape[:-1], weight.shape[0]))
