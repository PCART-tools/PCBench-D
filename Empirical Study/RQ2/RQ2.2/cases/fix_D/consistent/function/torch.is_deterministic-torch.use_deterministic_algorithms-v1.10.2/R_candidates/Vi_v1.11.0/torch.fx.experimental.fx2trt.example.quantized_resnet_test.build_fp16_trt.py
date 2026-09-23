def build_fp16_trt(rn18):
    rn18 = copy.deepcopy(rn18)
    rn18 = acc_tracer.trace(rn18, [torch.randn(1, 3, 224, 224)])
    interp = TRTInterpreter(
        rn18, [InputTensorSpec(torch.Size([3, 224, 224]), torch.float, has_batch_dim=False)])
    interpreter_result = interp.run(fp16_mode=True)
    return TRTModule(interpreter_result.engine, interpreter_result.input_names, interpreter_result.output_names)
