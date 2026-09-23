def invoke_subgraph_placeholder(func, *args, **kwargs):
    if torch.compiler.is_dynamo_compiling():
        # This is just a placeholder for Dynamo to replace with invoke_subgraph
        raise RuntimeError("invoke_subgraph should not be called directly in Dynamo")

    if torch.compiler.is_compiling():
        # For non-strict export tracing, we still want to go through Dynamo
        from torch._dynamo.backends.debugging import (
            make_eager_backend_with_torch_function_mode,
        )

        def _invoke_subgraph_placeholder_wrapper(func, args):
            return invoke_subgraph_placeholder(func, *args)

        with _set_compilation_env(), torch._dynamo.utils.disable_cache_limit(), _temp_remove_pre_dispatch_torch_function_mode():
            with _temp_remove_metadata_torch_function_mode() as metadata_mode:
                if metadata_mode:
                    backend = make_eager_backend_with_torch_function_mode(metadata_mode)
                else:
                    backend = "eager"

                return torch.compile(
                    _invoke_subgraph_placeholder_wrapper,
                    backend=backend,
                    fullgraph=True,
                )(func, args)

    return func(*args, **kwargs)
