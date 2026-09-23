def lower_mod_default(
    mod: torch.fx.GraphModule, inputs: Tensors, batch_size: Any = 2048
) -> TRTModule:
    interp = TRTInterpreter(
        mod, InputTensorSpec.from_tensors(inputs), explicit_batch_dimension=True
    )
    interpreter_result = interp.run(max_batch_size=batch_size)
    res_mod = TRTModule(interpreter_result.engine, interpreter_result.input_names, interpreter_result.output_names)
    return res_mod
