def lower_to_trt(model, inputs, shape_ranges):
    """ Lower a quantized model to TensorRT
    """
    assert len(inputs) == 1, "lower_to_trt only works for one input currently"
    model = acc_tracer.trace(model, inputs)  # type: ignore[attr-defined]
    # TODO: test multiple inputs setting and enable multiple inputs
    input_specs = [
        InputTensorSpec(
            torch.Size([-1, *inputs[0].shape[1:]]), torch.float,
            shape_ranges=shape_ranges, has_batch_dim=True)
    ]

    interp = TRTInterpreter(
        model,
        input_specs,
        explicit_batch_dimension=True, explicit_precision=True)
    result = interp.run(fp16_mode=False, int8_mode=True)
    trt_mod = TRTModule(result.engine, result.input_names, result.output_names)
    return trt_mod
