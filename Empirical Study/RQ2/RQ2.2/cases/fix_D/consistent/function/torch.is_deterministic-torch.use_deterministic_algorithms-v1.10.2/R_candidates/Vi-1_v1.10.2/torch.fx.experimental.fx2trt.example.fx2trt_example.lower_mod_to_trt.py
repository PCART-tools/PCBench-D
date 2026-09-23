def lower_mod_to_trt(mod: torch.fx.GraphModule, inputs: Tuple[torch.Tensor]):
    """
    Helper function that given a GraphModule `mod` and its `inputs`, build a
    TRTModule that runs the original `mod` on TensorRT.
    """
    interp = TRTInterpreter(mod, InputTensorSpec.from_tensors(inputs))
    engine, input_names, output_names = interp.run(*inputs)
    return TRTModule(engine, input_names, output_names)
