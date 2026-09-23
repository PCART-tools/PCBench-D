def compile_or_get_cached(backend, computation, compile_options,
                          host_callbacks):
  # Avoid import cycle between jax and jax.experimental
  from jax.experimental.compilation_cache import compilation_cache as cc

  if isinstance(computation, ir.Module):
    sym_name = computation.operation.attributes['sym_name']
    module_name = ir.StringAttr(sym_name).value
    # Convert ir.Module to str representation (the default), unless the
    # back-end expliclity flags the ability to handle a module directly
    # (avoiding the overhead of back and forth conversions)
    if getattr(backend, "needs_str_ir", True):
      computation = mlir.module_to_string(computation)
  else:
    module_name = computation.name()

  # Persistent compilation cache only implemented on TPU.
  # TODO(skye): add warning when initializing cache on unsupported default platform
  if cc.is_initialized() and backend.platform == 'tpu':
    cached_executable = cc.get_executable(computation, compile_options, backend)
    if cached_executable is not None:
      logging.info('Persistent compilation cache hit for %s.', module_name)
      return cached_executable
    else:
      compiled = backend_compile(backend, computation, compile_options,
                                 host_callbacks)
      cc.put_executable(module_name, computation, compile_options, compiled,
                        backend)
      return compiled

  if FLAGS.jax_dump_ir_to:
    if isinstance(computation, xc.XlaComputation):
      ir_str = computation.as_hlo_text()
    elif isinstance(computation, ir.Module):
      ir_str = mlir.module_to_string(computation)
    else:
      assert isinstance(computation, str)
      ir_str = computation
    _dump_ir_to_file(module_name, ir_str)
  return backend_compile(backend, computation, compile_options, host_callbacks)
