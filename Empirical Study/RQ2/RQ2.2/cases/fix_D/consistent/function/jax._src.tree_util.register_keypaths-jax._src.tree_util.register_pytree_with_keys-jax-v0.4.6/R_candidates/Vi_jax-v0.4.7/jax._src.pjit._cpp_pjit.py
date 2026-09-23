def _cpp_pjit(fun: Callable, infer_params_fn, static_argnums, static_argnames,
              donate_argnums, pjit_has_explicit_sharding):

  @api_boundary
  def cache_miss(*args, **kwargs):
    outs, out_flat, out_tree, args_flat = _python_pjit_helper(
        fun, infer_params_fn, *args, **kwargs)

    executable = _read_most_recent_pjit_call_executable()

    use_fastpath = (
        executable is not None and
        isinstance(executable, pxla.MeshExecutable) and
        isinstance(executable.unsafe_call, pxla.ExecuteReplicated) and
        # No effects in computation
        not executable.unsafe_call.ordered_effects and
        not executable.unsafe_call.has_unordered_effects and
        not executable.unsafe_call.has_host_callbacks and
        all(isinstance(x, xc.ArrayImpl) for x in out_flat)
    )

    if use_fastpath:
      out_avals = [o.aval for o in out_flat]
      out_committed = [o._committed for o in out_flat]
      kept_var_bitvec = [i in executable._kept_var_idx
                         for i in range(len(args_flat))]
      fastpath_data = pxla.MeshExecutableFastpathData(
          executable.xla_executable, out_tree, executable._in_shardings,
          executable._out_shardings, out_avals, out_committed, kept_var_bitvec)
    else:
      fastpath_data = None

    return outs, fastpath_data

  if pjit_has_explicit_sharding:
    global_cache = xc._xla.PjitFunctionCache()
  else:
    global_cache = _cpp_pjit_cache
  cpp_pjit_f = xc._xla.pjit(  # type: ignore
      getattr(fun, "__name__", "<unnamed function>"),  # type: ignore
      fun, cache_miss, static_argnums, static_argnames,  # type: ignore
      donate_argnums, global_cache)  # type: ignore

  cpp_pjitted_f = wraps(fun)(cpp_pjit_f)
  cpp_pjitted_f._fun = fun
  type(cpp_pjitted_f).clear_cache = _cpp_pjit_evict_fn
  return cpp_pjitted_f
