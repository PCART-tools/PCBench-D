@torch.no_grad()
def build_int8_trt(rn18):
    rn18 = copy.deepcopy(rn18)
    data = torch.randn(1, 3, 224, 224)
    # data = torch.randn(1, 32)
    # data = torch.randn(1, 64, 10, 10)
    # TensorRT only supports symmetric quantization
    qconfig = torch.ao.quantization.QConfig(
        activation=torch.ao.quantization.observer.HistogramObserver.with_args(
            qscheme=torch.per_tensor_symmetric, dtype=torch.qint8
        ),
        # weight=torch.ao.quantization.default_weight_observer
        # uncomment to check per channel quant works
        weight=torch.quantization.default_per_channel_weight_observer
    )
    prepared = prepare_fx(rn18, {"": qconfig})
    for _ in range(10):
        prepared(data)
    quantized_rn18 = convert_fx(prepared, is_reference=True)
    ref_res = quantized_rn18(data)
    print("quantized model:", quantized_rn18)

    quantized_rn18 = acc_tracer.trace(quantized_rn18, [data])  # type: ignore[assignment]
    interp = TRTInterpreter(
        quantized_rn18,
        [InputTensorSpec(torch.Size([-1, *data.shape[1:]]), torch.float,
                         shape_ranges=[((1, 3, 224, 224), (5, 3, 224, 224), (10, 3, 224, 224))], has_batch_dim=True)],
        explicit_batch_dimension=True, explicit_precision=True, logger_level=trt.Logger.VERBOSE)
    interpreter_result = interp.run(fp16_mode=False, int8_mode=True)
    trt_mod = TRTModule(interpreter_result.engine, interpreter_result.input_names, interpreter_result.output_names)
    trt_res = trt_mod(data.cuda())
    print("explicit quant result diff max", torch.max(ref_res - trt_res.cpu()))
    return trt_mod
