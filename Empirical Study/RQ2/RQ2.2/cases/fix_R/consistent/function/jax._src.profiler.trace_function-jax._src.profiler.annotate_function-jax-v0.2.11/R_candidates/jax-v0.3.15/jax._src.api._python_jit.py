def _python_jit(
    fun: Callable,
    *,
    static_argnums: Tuple[int, ...],
    static_argnames: Tuple[str, ...],
    device: Optional[xc.Device],
    backend: Optional[str],
    donate_argnums: Tuple[int, ...],
    inline: bool,
    keep_unused: bool,
    abstracted_axes: Optional[PytreeOfAbstractedAxesSpec],
  ) -> stages.Wrapped:
  @wraps(fun)
  @api_boundary
  def f_jitted(*args, **kwargs):
    if config.jax_disable_jit:
      return fun(*args, **kwargs)
    closed_fun, in_tree, args_flat, donated_invars = _prepare_jit(
        fun, static_argnums, static_argnames, donate_argnums, args, kwargs)
    flat_fun, out_tree = flatten_fun(closed_fun, in_tree)
    for arg in args_flat:
      _check_arg(arg)
    if jax.config.jax_dynamic_shapes:
      axes_specs = (None if abstracted_axes is None else
                    _flat_axes_specs(abstracted_axes, *args, **kwargs))
      in_type = pe.infer_lambda_input_type(axes_specs, args_flat)
      flat_fun = lu.annotate(flat_fun, in_type)
    out_flat = xla.xla_call(
        flat_fun, *args_flat,
        device=device, backend=backend, name=flat_fun.__name__,
        donated_invars=donated_invars, inline=inline,
        keep_unused=keep_unused)
    return tree_unflatten(out_tree(), out_flat)

  f_jitted.lower = _jit_lower(fun, static_argnums, static_argnames, device,
                              backend, donate_argnums, inline, keep_unused,
                              abstracted_axes)

  def clear_cache():
    dispatch.xla_callable.evict_function(fun)
  f_jitted.clear_cache = clear_cache

  return f_jitted
