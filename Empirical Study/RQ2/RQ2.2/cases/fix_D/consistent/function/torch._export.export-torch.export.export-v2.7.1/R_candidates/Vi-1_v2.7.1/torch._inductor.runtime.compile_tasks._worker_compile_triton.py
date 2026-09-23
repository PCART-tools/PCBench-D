def _worker_compile_triton(
    load_kernel: Callable[[], CachingAutotuner], extra_env: dict[str, str]
) -> tuple[CachingAutotuner, int]:
    _set_triton_ptxas_path()
    os.environ.update(extra_env)
    start_ns = time.time_ns()
    kernel = load_kernel()
    kernel.precompile(warm_cache_only=True)
    elapsed_ns = time.time_ns() - start_ns
    kernel.prepare_for_pickle()
    return kernel, elapsed_ns // 1000
