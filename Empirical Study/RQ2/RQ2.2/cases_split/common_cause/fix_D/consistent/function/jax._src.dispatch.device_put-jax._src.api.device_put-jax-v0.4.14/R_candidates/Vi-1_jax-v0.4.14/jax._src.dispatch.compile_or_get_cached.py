def compile_or_get_cached(backend, computation: ir.Module, devices: np.ndarray,
                          compile_options, host_callbacks):
  sym_name = computation.operation.attributes['sym_name']
  module_name = ir.StringAttr(sym_name).value

  if _DUMP_IR_TO.value:
    _dump_ir_to_file(module_name, mlir.module_to_string(computation))

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

  cache_key = compilation_cache.get_cache_key(
      computation, devices, compile_options, backend)

  executable, compile_time_retrieved = _cache_read(
      module_name, cache_key, compile_options, backend)
  if executable is not None:
    # TODO(b/289098047): Will instrument a metric which uses the 'compile_time'
    # to measure the savings due to the cache hit.
    logger.info("Persistent compilation cache hit for '%s'", module_name)
    return executable
  else:
    start_time = time.monotonic()
    executable = backend_compile(backend, computation,
                                compile_options, host_callbacks)
    compile_time = time.monotonic() - start_time
    _cache_write(cache_key, compile_time, module_name, backend, executable,
                 host_callbacks)
    return executable
