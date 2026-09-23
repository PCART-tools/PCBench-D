@parse_args("v", "is", "v", "v", "f", "i")
def layer_norm(g, input, normalized_shape, weight, bias, eps, cudnn_enable):
    if sym_help._operator_export_type == torch.onnx.OperatorExportTypes.ONNX_ATEN_FALLBACK:
        return g.op("ATen", input, weight, bias, normalized_shape_i=normalized_shape,
                    eps_f=eps, cudnn_enable_i=cudnn_enable, operator_s="layer_norm")

    axes = [-i for i in range(len(normalized_shape), 0, -1)]

    two_cst = sym_help._generate_wrapped_number(g, 2.)
    eps_cst = sym_help._generate_wrapped_number(g, eps)

    mean = g.op("ReduceMean", input, axes_i=axes)
    numerator = sub(g, input, mean)
    # variance = e((x - e(x))^2), and (x - e(x)) is the numerator in the layer_norm formula
    variance = g.op("ReduceMean", pow(g, numerator, two_cst), axes_i=axes)
    denominator = sqrt(g, add(g, variance, eps_cst))

    layer_norm = g.op("Div", numerator, denominator)

    if not (weight is None or sym_help._is_none(weight)):
        layer_norm = mul(g, layer_norm, weight)
    if not (bias is None or sym_help._is_none(bias)):
        layer_norm = add(g, layer_norm, bias)

    return layer_norm
