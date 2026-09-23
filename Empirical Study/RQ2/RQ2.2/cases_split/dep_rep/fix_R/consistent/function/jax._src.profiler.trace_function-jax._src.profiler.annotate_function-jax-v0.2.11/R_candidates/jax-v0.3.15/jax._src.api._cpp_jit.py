def _cpp_jit(
    fun: Callable,
    *,
    static_argnums: Tuple[int, ...],
    static_argnames: Tuple[str, ...],
    device: Optional[xc.Device],
    backend: Optional[str],
    donate_argnums: Tuple[int, ...],
    inline: bool,
    keep_unused: bool,
  ) -> stages.Wrapped:
  # An implementation of `jit` that tries to do as much as possible in C++.
  # The goal of this function is to speed up the time it takes to process the
  # arguments, find the correct C++ executable, start the transfer of arguments
  # and schedule the computation.
  # As long as it does not support all features of the Python implementation
  # the C++ code will fallback to `_python_jit` when it faces some unsupported
  # feature.
  if device is not None and backend is not None:
    raise ValueError("can't specify both a device and a backend for jit, "
                     f"got device={device} and backend={backend}.")

  @api_boundary
  def cache_miss(*args, **kwargs):
    ### This first part is basically the same code as in _python_jit.
    # An alternative would be for cache_miss to accept from C++ the arguments
    # (dyn_args, donated_invars, args_flat, in_tree), since otherwise we have
    # work/code that is redundant between C++ and Python. We can try that later.
    closed_fun, in_tree, args_flat, donated_invars = _prepare_jit(
        fun, static_argnums, static_argnames, donate_argnums, args, kwargs)
    for arg in args_flat:
      _check_arg(arg)
    flat_fun, out_tree = flatten_fun(closed_fun, in_tree)
    if jax.config.jax_dynamic_shapes:
      in_type = pe.infer_lambda_input_type(None, args_flat)
      flat_fun = lu.annotate(flat_fun, in_type)
    out_flat = xla.xla_call(
        flat_fun, *args_flat,
        device=device, backend=backend, name=flat_fun.__name__,
        donated_invars=donated_invars, inline=inline, keep_unused=keep_unused)
    out_pytree_def = out_tree()
    out = tree_unflatten(out_pytree_def, out_flat)

    ### Decide whether we can support the C++ fast path
    # High level note: The Python tracing mechanism is complex; in particular
    # to know whether `jax.jit(f)(x)` will execute or trace, it's not enough to
    # inspect the argument x, we actually do need to execute it and look at the
    # outputs that could be tracers (if f is capturing `Tracer` by closure).
    execute: Optional[functools.partial] = (
        dispatch.xla_callable.most_recent_entry())
    # TODO(sharadmv): Enable fast path for effectful jaxprs
    # TODO(sharadmv): Clean up usage of `execute.args`
    use_fastpath = (
        # This is if we have already executed this code-path (most-recent entry
        # has been reset to None). Thus, we do not support the fast-path.
        execute is not None and
        execute.func is dispatch._execute_compiled and  # not trivial, not pmap
        # No effects in computation
        not execute.args[5] and
        not execute.args[6] and
        # Not supported: ShardedDeviceArray
        all(device_array.type_is_device_array(x) for x in out_flat) and
        # Not supported: dynamic shapes
        not jax.config.jax_dynamic_shapes and
        type(execute.args[4]) is dispatch.SimpleResultHandler
    )
    ### If we can use the fastpath, we return required info to the caller.
    if use_fastpath:
      (_, xla_executable,
       _, _, result_handlers, _, _, kept_var_idx) = execute.args
      sticky_device = None
      avals = []
      lazy_exprs = [None] * len(result_handlers)
      for result_handler in result_handlers:
        aval, sticky_device = result_handler.args
        avals.append(aval)
      assert len(avals) == len(out_flat)
      kept_var_bitvec = [i in kept_var_idx for i in range(len(args_flat))]
      fastpath_data = _FastpathData(xla_executable, out_pytree_def,
                                    sticky_device, avals, lazy_exprs,
                                    kept_var_bitvec)
    else:
      fastpath_data = None

    return out, fastpath_data

  def get_device_info():
    """Backends do not exist before __main__ is being executed."""
    committed_to_device = device is not None or backend is not None

    if device is not None:
      default_device = device
    else:
      backend_ = xb.get_backend(backend)
      default_device = backend_.get_default_device_assignment(1)[0]

    return _BackendAndDeviceInfo(default_device, committed_to_device)

  jitted_f_kwargs = {}
  jitted_f_kwargs["has_explicit_device"] = (
      device is not None or backend is not None)
  cpp_jitted_f = jax_jit.jit(
      fun,
      cache_miss,
      get_device_info,
      static_argnums=static_argnums,
      static_argnames=static_argnames,
      donate_argnums=donate_argnums,
      cache=_cpp_jit_cache,
      **jitted_f_kwargs)  # type: ignore
  f_jitted = wraps(fun)(cpp_jitted_f)

  f_jitted.lower = _jit_lower(fun, static_argnums, static_argnames, device,
                              backend, donate_argnums, inline, keep_unused,
                              None)
  f_jitted._fun = fun
  type(f_jitted).clear_cache = _cpp_jit_clear_cache

  return f_jitted
