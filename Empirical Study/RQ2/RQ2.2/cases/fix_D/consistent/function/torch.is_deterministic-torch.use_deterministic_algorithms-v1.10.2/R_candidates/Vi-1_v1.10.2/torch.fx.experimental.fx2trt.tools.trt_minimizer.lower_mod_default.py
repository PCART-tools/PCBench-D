def lower_mod_default(
    mod: torch.fx.GraphModule, inputs: Tensors, batch_size: Any = 2048
) -> TRTModule:
    interp = TRTInterpreter(
        mod, InputTensorSpec.from_tensors(inputs), explicit_batch_dimension=True
    )
    res_mod = TRTModule(*interp.run(max_batch_size=batch_size))
    return res_mod
