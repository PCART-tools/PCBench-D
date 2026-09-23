@parse_args("v", "is", "i", "i")
def _var_mean(g, input, dim, correction, keepdim):
    if dim is None:
        mean = g.op("ReduceMean", input, keepdims_i=0)
        t_mean = mean
        num_elements = numel(g, input)
    else:
        mean = g.op("ReduceMean", input, axes_i=dim, keepdims_i=keepdim)
        t_mean = g.op("ReduceMean", input, axes_i=dim, keepdims_i=1)
        redudced_dims = g.op("Shape", input)
        # dim could contain one or multiple dimensions
        redudced_dims = g.op("Gather", redudced_dims, g.op("Constant", value_t=torch.tensor(dim)), axis_i=0)
        num_elements = g.op("ReduceProd", redudced_dims, keepdims_i=0)
    sub_v = g.op("Sub", input, t_mean)
    sqr_sub = g.op("Mul", sub_v, sub_v)
    keepdim_mean = 0 if dim is None else keepdim
    var = g.op("ReduceMean", sqr_sub, axes_i=dim, keepdims_i=keepdim_mean)
    # Correct bias in calculating variance, by dividing it over (N - correction) instead on N
    if correction is None:
        correction = 1
    if correction != 0:
        num_elements = g.op("Cast", num_elements, to_i=sym_help.cast_pytorch_to_onnx["Float"])
        one = g.op("Constant", value_t=torch.tensor(correction, dtype=torch.float))
        mul = g.op("Mul", var, num_elements)
        var = g.op("Div", mul, g.op("Sub", num_elements, one))
    return var, mean
