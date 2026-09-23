def _cpp_pjit(fun: Callable, infer_params_fn, static_argnums, static_argnames,
              donate_argnums, pjit_has_explicit_sharding):

  @api_boundary
  def cache_miss(*args, **kwargs):
    outs, out_flat, out_tree, args_flat, jaxpr = _python_pjit_helper(
        fun, infer_params_fn, *args, **kwargs)
    executable = _read_most_recent_pjit_call_executable(jaxpr)
    fastpath_data = _get_fastpath_data(executable, out_tree, args_flat, out_flat)
    return outs, fastpath_data

  if xla_extension_version >= 169:
    cpp_pjit_f = xc._xla.pjit(  # type: ignore
      getattr(fun, "__name__", "<unnamed function>"),  # type: ignore
      fun, cache_miss, static_argnums, static_argnames,  # type: ignore
      donate_argnums, tree_util.default_registry,  # type: ignore
      _get_cpp_global_cache(pjit_has_explicit_sharding))  # type: ignore
  else:
    cpp_pjit_f = xc._xla.pjit(  # type: ignore
      getattr(fun, "__name__", "<unnamed function>"),  # type: ignore
      fun, cache_miss, static_argnums, static_argnames,  # type: ignore
      donate_argnums, _get_cpp_global_cache(pjit_has_explicit_sharding))  # type: ignore


  cpp_pjitted_f = wraps(fun)(cpp_pjit_f)
  cpp_pjitted_f._fun = fun
  type(cpp_pjitted_f).clear_cache = _cpp_pjit_evict_fn
  return cpp_pjitted_f
