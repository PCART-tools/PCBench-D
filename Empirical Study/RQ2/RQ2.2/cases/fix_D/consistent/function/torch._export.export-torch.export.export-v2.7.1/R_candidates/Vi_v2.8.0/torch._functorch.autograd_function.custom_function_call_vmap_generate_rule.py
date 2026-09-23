def custom_function_call_vmap_generate_rule(interpreter, autograd_function, *operands):
    unwrapped_operands, in_dims = unwrap_batched(operands, interpreter.level())
    vmapped_function = vmapify_autograd_function(
        autograd_function, in_dims, interpreter.batch_size(), interpreter.randomness()
    )
    with interpreter.lower():
        outputs = custom_function_call(vmapped_function, *unwrapped_operands)

    assert isinstance(outputs, tuple)
    outputs, out_dims = unpack_outputs(outputs)
    return wrap_batched(outputs, out_dims, interpreter.level())
