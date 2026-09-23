@_onnx_symbolic("aten::nan_to_num")
@symbolic_helper.parse_args("v", "f", "f", "f")
def nan_to_num(g: jit_utils.GraphContext, input, nan, posinf, neginf):
    # Cannot create a int type tensor with inf/nan values, so we simply
    # return the original tensor
    if not symbolic_helper._is_fp(input):
        return input
    input_dtype = _type_utils.JitScalarType.from_value(input).dtype()
    if nan is None:
        nan = 0.0
    nan_cond = opset9.isnan(g, input)
    nan_result = g.op(
        "Where",
        nan_cond,
        g.op("Constant", value_t=torch.tensor([nan], dtype=input_dtype)),
        input,
    )

    # For None values of posinf, neginf we use the greatest/lowest finite
    # value representable by input's dtype.
    finfo = torch.finfo(input_dtype)
    if posinf is None:
        posinf = finfo.max
    posinf_cond = opset9.logical_and(
        g,
        isinf(g, nan_result),
        opset9.gt(g, nan_result, g.op("Constant", value_t=torch.LongTensor([0]))),
    )
    nan_posinf_result = g.op(
        "Where",
        posinf_cond,
        g.op("Constant", value_t=torch.tensor([posinf], dtype=input_dtype)),
        nan_result,
    )

    if neginf is None:
        neginf = finfo.min
    neginf_cond = opset9.logical_and(
        g,
        isinf(g, nan_posinf_result),
        opset9.lt(
            g, nan_posinf_result, g.op("Constant", value_t=torch.LongTensor([0]))
        ),
    )
    return g.op(
        "Where",
        neginf_cond,
        g.op("Constant", value_t=torch.tensor([neginf], dtype=input_dtype)),
        nan_posinf_result,
    )
