@parse_args("v", "i", "b", "v")
def multinomial(g, input, num_samples, replacement=False, generator=None):
    if generator is not None and not sym_help._is_none(generator):
        _unimplemented("Multinomial", "generator is not supported for multinomial")
    if not replacement and num_samples > 1:
        _unimplemented("Multinomial", "replacement=False when num_samples > 1 is not supported for multinomial")

    log_input = log(g, input)
    return g.op("Multinomial", log_input,
                dtype_i=sym_help.cast_pytorch_to_onnx["Long"],
                sample_size_i=num_samples)
