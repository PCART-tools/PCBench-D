def compile_or_get_cached(
    backend: xc.Client,
    computation: ir.Module,
    devices: np.ndarray,
    compile_options: xc.CompileOptions,
    host_callbacks: Sequence[Any],
) -> xc.LoadedExecutable:
  sym_name = computation.operation.attributes['sym_name']
  module_name = ir.StringAttr(sym_name).value

  if _DUMP_IR_TO.value:
    _dump_ir_to_file(module_name, _module_to_string(computation))

  # Persistent compilation cache only implemented on TPU and GPU.
  # TODO(skye): add warning when initializing cache on unsupported default platform
  supported_platforms = ["tpu", "gpu"]
  # (b/233850967) CPU caching can be enabled if XLA Runtime is enabled.
  if "--xla_cpu_use_xla_runtime=true" in os.environ.get("XLA_FLAGS", ""):
    supported_platforms.append("cpu")
  use_compilation_cache = (compilation_cache.is_initialized() and
                           backend.platform in supported_platforms)

  if not use_compilation_cache:
    return backend_compile(backend, computation, compile_options,
                           host_callbacks)

  # TODO(b/293308239) Instrument a metric to track the adoption of the new cache
  # key implementation once the enabling flag is added.
  global _cache_used
  if not _cache_used:
    _cache_used = True
    monitoring.record_event('/jax/compilation_cache/tasks_using_original_cache')

  cache_key = compilation_cache.get_cache_key(
      computation, devices, compile_options, backend,
      jax_config.config.jax_use_original_compilation_cache_key_generation,
  )

  cache_retrieval_start = time.monotonic()
  retrieved_executable, retrieved_compile_time = _cache_read(
      module_name, cache_key, compile_options, backend)
  cache_retrieval_time = time.monotonic() - cache_retrieval_start

  if retrieved_executable is not None:
    assert retrieved_compile_time is not None
    logger.info("Persistent compilation cache hit for '%s'", module_name)
    monitoring.record_event_duration_secs(
        "/jax/compilation_cache/cache_retrieval_time_sec", cache_retrieval_time)
    # TODO(b/293308239) Instrument a metric for new cache savings once the
    # enabling flag is added.
    # TODO(b/293308239) Remove the metric for original cache savings after the
    # new compilation cache key implementation is fully rolled out.
    monitoring.record_event_duration_secs(
        "/jax/compilation_cache/original_compile_time_saved_sec",
        retrieved_compile_time - cache_retrieval_time)
    return retrieved_executable
  else:
    start_time = time.monotonic()
    executable = backend_compile(backend, computation,
                                compile_options, host_callbacks)
    compile_time = time.monotonic() - start_time
    _cache_write(cache_key, compile_time, module_name, backend, executable,
                 host_callbacks)
    return executable
