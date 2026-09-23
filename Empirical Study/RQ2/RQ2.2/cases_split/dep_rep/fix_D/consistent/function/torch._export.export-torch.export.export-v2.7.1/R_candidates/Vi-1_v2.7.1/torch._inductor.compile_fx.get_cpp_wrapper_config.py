def get_cpp_wrapper_config() -> dict[str, object]:
    if config.triton.cudagraphs:
        log_cudagraph_skip_and_bump_counter(
            format_default_skip_message("cpp wrapper enabled")
        )

    return {
        # Set autotune_at_compile_time to True as default if the option is not explicitly set
        "triton.autotune_at_compile_time": (
            config.triton.autotune_at_compile_time
            if config.triton.autotune_at_compile_time is not None
            else has_triton()
        ),
        "triton.autotune_cublasLt": False,
        "triton.cudagraphs": False,  # TODO: to be removed
        "triton.store_cubin": True,
    }
