def build_fp16_trt(rn18):
    rn18 = copy.deepcopy(rn18)
    rn18 = acc_tracer.trace(rn18, [torch.randn(1, 3, 224, 224)])
    interp = TRTInterpreter(
        rn18, [InputTensorSpec(torch.Size([3, 224, 224]), torch.float, has_batch_dim=False)])
    engine, input_names, output_names = interp.run(fp16_mode=True)
    return TRTModule(engine, input_names, output_names)
