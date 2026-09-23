@_onnx_symbolic("aten::constant_pad_nd")
def constant_pad_nd(g: jit_utils.GraphContext, input, padding, value):
    mode = "constant"
    try:
        value = symbolic_helper._get_const(value, "f", "value")
    except Exception:
        # FIXME(justinchuby): Avoid catching Exception.
        # Catch a more specific exception instead.
        return symbolic_helper._onnx_opset_unsupported_detailed(
            "Pad", 9, 11, "The value for the padding must be constant", value
        )

    padding = _convert_padding_node(padding)
    paddings = _prepare_onnx_paddings(symbolic_helper._get_tensor_rank(input), padding)
    return symbolic_helper._op_with_optional_float_cast(
        g, "Pad", input, pads_i=paddings, mode_s=mode, value_f=value, opset_before=11
    )
