@_onnx_symbolic("aten::multinomial")
@symbolic_helper.parse_args("v", "i", "b", "v")
def multinomial(
    g: jit_utils.GraphContext, input, num_samples, replacement=False, generator=None
):
    if generator is not None and not symbolic_helper._is_none(generator):
        symbolic_helper._unimplemented(
            "Multinomial", "generator is not supported for multinomial", input
        )
    if not replacement and num_samples > 1:
        symbolic_helper._unimplemented(
            "Multinomial",
            "replacement=False when num_samples > 1 is not supported for multinomial",
            input,
        )

    log_input = log(g, input)
    return g.op(
        "Multinomial",
        log_input,
        dtype_i=_C_onnx.TensorProtoDataType.INT64,
        sample_size_i=num_samples,
    )
