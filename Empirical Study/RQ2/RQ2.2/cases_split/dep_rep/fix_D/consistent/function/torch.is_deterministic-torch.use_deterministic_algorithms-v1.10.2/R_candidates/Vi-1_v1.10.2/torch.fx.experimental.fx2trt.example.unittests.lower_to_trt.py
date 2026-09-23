def lower_to_trt(model, sample_input, shape_ranges):
    model = acc_tracer.trace(model, [sample_input])  # type: ignore[attr-defined]
    interp = TRTInterpreter(
        model,
        [InputTensorSpec(
            torch.Size([-1, *sample_input.shape[1:]]), torch.float,
            shape_ranges=shape_ranges, has_batch_dim=True)],
        explicit_batch_dimension=True, explicit_precision=True)
    engine, input_names, output_names = interp.run(fp16_mode=False, int8_mode=True)
    trt_mod = TRTModule(engine, input_names, output_names)
    return trt_mod
