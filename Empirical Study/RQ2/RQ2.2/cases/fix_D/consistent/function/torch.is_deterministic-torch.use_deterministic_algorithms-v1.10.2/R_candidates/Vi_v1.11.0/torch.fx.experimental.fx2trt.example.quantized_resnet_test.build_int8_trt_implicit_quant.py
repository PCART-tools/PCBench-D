@torch.no_grad()
def build_int8_trt_implicit_quant(rn18):
    rn18 = copy.deepcopy(rn18)
    data = torch.randn(1, 3, 224, 224)
    # Quantization
    qconfig = torch.ao.quantization.QConfig(
        activation=torch.ao.quantization.observer.HistogramObserver.with_args(
            qscheme=torch.per_tensor_symmetric, reduce_range=True
        ),
        weight=torch.ao.quantization.default_per_channel_weight_observer
    )
    prepared = prepare_fx(rn18, {"": qconfig})
    for _ in range(10):
        prepared(data)
    quantized_rn18 = convert_fx(prepared)
    ref_res = quantized_rn18(data)

    # Build trt int8 model
    traced_rn18 = torch.fx.symbolic_trace(quantized_rn18)
    shape_prop.ShapeProp(traced_rn18).propagate(data)
    traced_rn18 = NormalizeArgs(traced_rn18).transform()
    interp = TRTInterpreter(traced_rn18, InputTensorSpec.from_tensors([data]), logger_level=trt.Logger.VERBOSE)
    interpreter_result = interp.run(fp16_mode=False, int8_mode=True, strict_type_constraints=True)
    trt_mod = TRTModule(interpreter_result.engine, interpreter_result.input_names, interpreter_result.output_names)
    trt_res = trt_mod(data.cuda())
    print("implicit quant result diff max", torch.max(ref_res - trt_res.cpu()))
    return trt_mod
