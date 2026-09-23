def _maybe_compile_and_run_fn(fn, *args):
    if not torch.compiler.is_dynamo_compiling():
        from torch._dynamo.backends.debugging import (
            make_eager_backend_with_torch_function_mode,
        )

        with _set_compilation_env(), torch._dynamo.utils.disable_cache_limit():
            with _temp_remove_metadata_torch_function_mode() as metadata_mode:
                if metadata_mode:
                    backend = make_eager_backend_with_torch_function_mode(metadata_mode)
                else:
                    backend = "eager"
                return torch.compile(fn, backend=backend, fullgraph=True)(*args)
    else:
        return fn(*args)
