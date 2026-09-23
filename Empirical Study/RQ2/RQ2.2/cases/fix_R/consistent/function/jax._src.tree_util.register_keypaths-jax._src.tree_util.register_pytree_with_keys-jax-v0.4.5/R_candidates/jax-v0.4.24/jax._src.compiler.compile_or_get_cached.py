def compile_or_get_cached(
    backend: xc.Client,
    computation: ir.Module,
    devices: np.ndarray,
    compile_options: xc.CompileOptions,
    host_callbacks: Sequence[Any],
) -> xc.LoadedExecutable:
  sym_name = computation.operation.attributes['sym_name']
  module_name = ir.StringAttr(sym_name).value

  if dumped_to := mlir.dump_module_to_file(computation, "compile"):
    logging.info("Dumped the module to %s.", dumped_to)

  # Persistent compilation cache only implemented on TPU and GPU.
  # TODO(skye): add warning when initializing cache on unsupported default platform
  supported_platforms = ["tpu", "gpu"]
  # TODO(b/323256224): Add back support for CPU together with extra fields in a
  # cache key with underlying hardware features (xla_extension_version >= 230).
  use_compilation_cache = (config.enable_compilation_cache.value and
                           backend.platform in supported_platforms)

  if not use_compilation_cache:
    return backend_compile(backend, computation, compile_options,
                           host_callbacks)

  compilation_cache.set_once_cache_used(
      lambda: monitoring.record_event(
          "/jax/compilation_cache/tasks_using_cache"))
  monitoring.record_event('/jax/compilation_cache/compile_requests_use_cache')

  try:
    cache_key = compilation_cache.get_cache_key(
        computation, devices, compile_options, backend)
  except xc._xla.XlaRuntimeError as ex:
    logger.error("compile_or_get_cached: unable to generate cache key, "
                 "skipping the cache: %s", ex)
    return backend_compile(backend, computation, compile_options,
                           host_callbacks)

  cache_retrieval_start = time.monotonic()
  retrieved_executable, retrieved_compile_time = _cache_read(
      module_name, cache_key, compile_options, backend)
  cache_retrieval_time = time.monotonic() - cache_retrieval_start

  if retrieved_executable is not None:
    assert retrieved_compile_time is not None
    logger.debug("Persistent compilation cache hit for '%s'", module_name)

    monitoring.record_event('/jax/compilation_cache/cache_hits')
    monitoring.record_event_duration_secs(
        '/jax/compilation_cache/compile_time_saved_sec',
        retrieved_compile_time - cache_retrieval_time)

    monitoring.record_event_duration_secs(
        "/jax/compilation_cache/cache_retrieval_time_sec", cache_retrieval_time)

    return retrieved_executable
  elif (
      process_count() > 1
      and config.share_binary_between_hosts.value
      and distributed.global_state.client is not None
      # Host callbacks are currently baked into the HLO module so we cant share
      # them.
      and len(host_callbacks) == 0
  ):
    share_timeout = config.share_binary_between_hosts_timeout_ms.value
    global_client = distributed.global_state.client

    # TODO: Using module name as a cache key might lead to issues when the
    # the module with the same name should be recompiled. This cache should be
    # replaced with proper cache eviction logic based on barriers.
    if module_name in compile_or_get_cached.cached_modules:
      return compile_or_get_cached.cached_modules[module_name]

    # The coordinator host should compile the module and write it to the K-V
    # storage.
    # TODO: In case when coordinator process is not participating in the
    # computation we need to choose another host to compile the module.
    if distributed.global_state.service is None:
      serialized_executable = global_client.blocking_key_value_get_bytes(
          module_name, share_timeout)
      serialized_executable = compilation_cache.decompress_executable(
          serialized_executable)
      executable = backend.deserialize_executable(
          serialized_executable, compile_options)
    else:
      executable = backend_compile(backend, computation,
                                   compile_options, host_callbacks)
      serialized_executable = backend.serialize_executable(executable)
      serialized_executable = compilation_cache.compress_executable(
          serialized_executable)
      global_client.key_value_set(module_name, serialized_executable)

    compile_or_get_cached.cached_modules[module_name] = executable
    return executable
  else:
    start_time = time.monotonic()
    executable = backend_compile(backend, computation,
                                compile_options, host_callbacks)
    compile_time = time.monotonic() - start_time
    _cache_write(cache_key, compile_time, module_name, backend, executable,
                 host_callbacks)
    return executable
