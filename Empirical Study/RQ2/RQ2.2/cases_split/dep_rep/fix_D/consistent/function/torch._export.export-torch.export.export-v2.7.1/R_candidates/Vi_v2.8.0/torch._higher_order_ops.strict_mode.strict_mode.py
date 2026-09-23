@exposed_in("torch")
def strict_mode(callable, operands):
    from torch._dynamo.backends.debugging import (
        make_eager_backend_with_torch_function_modes,
    )

    if torch.compiler.is_dynamo_compiling():
        return strict_mode_op(callable, operands)

    with _set_compilation_env():
        with _temp_remove_metadata_torch_function_mode() as metadata_mode:
            with _temp_remove_pre_dispatch_torch_function_mode() as predispatch_mode:
                modes = [metadata_mode, predispatch_mode]
                modes = [mode for mode in modes if mode is not None]
                if modes:
                    backend = make_eager_backend_with_torch_function_modes(modes)
                else:
                    backend = "eager"
                with torch._dynamo.utils.disable_cache_limit():
                    return torch.compile(
                        strict_mode_op, backend=backend, fullgraph=True
                    )(callable, operands)
