def compile_or_get_cached(backend, computation: ir.Module, compile_options,
                          host_callbacks):
  # Avoid import cycle between jax and jax.experimental
  from jax.experimental.compilation_cache import compilation_cache as cc

  sym_name = computation.operation.attributes['sym_name']
  module_name = ir.StringAttr(sym_name).value

  if FLAGS.jax_dump_ir_to:
    _dump_ir_to_file(module_name, mlir.module_to_string(computation))

  # Convert ir.Module to a string representation, unless the
  # back-end expliclity flags the ability to handle a module directly
  # (avoiding the overhead of back and forth conversions)
  serialized_computation: Union[str, bytes, ir.Module]
  if getattr(backend, "needs_str_ir", True):
    serialized_computation = mlir.module_to_bytecode(computation)
  else:
    serialized_computation = computation

  # Persistent compilation cache only implemented on TPU and GPU.
  # TODO(skye): add warning when initializing cache on unsupported default platform
  supported_platforms = ["tpu", "gpu"]
  # (b/233850967) CPU caching can be enabled if XLA Runtime is enabled.
  if "--xla_cpu_use_xla_runtime=true" in os.environ.get("XLA_FLAGS", ""):
    supported_platforms.append("cpu")
  if cc.is_initialized() and backend.platform in supported_platforms:
    cached_executable = _cache_read(serialized_computation, module_name,
                                    compile_options, backend)
    if cached_executable is not None:
      logger.info("Persistent compilation cache hit for '%s'", module_name)
      return cached_executable
    else:
      start_time = time.monotonic()
      compiled = backend_compile(backend, serialized_computation,
                                 compile_options, host_callbacks)
      compile_time = time.monotonic() - start_time
      _cache_write(serialized_computation, compile_time, module_name,
                   compile_options, backend, compiled, host_callbacks)
      return compiled

  return backend_compile(backend, serialized_computation, compile_options,
                         host_callbacks)
