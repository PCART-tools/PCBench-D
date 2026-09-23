def _jit_lower(fun, static_argnums, static_argnames, device, backend,
               donate_argnums, inline,  keep_unused: bool,
               abstracted_axes: Optional[PytreeOfAbstractedAxesSpec]):
  """Make a ``lower`` method for jitted functions."""
  # If the function we returned from ``jit`` were a class instance,
  # this might naturally be a method, with ``fun`` as a ``self`` and
  # all the other arguments stored as attributes.

  def arg_spec(x):
    # like xla.arg_spec but duck-types on x.shape and x.dtype
    aval = None if jax.config.jax_dynamic_shapes else shaped_abstractify(x)
    device = getattr(x, '_device', None)
    return aval, device

  @api_boundary
  def lower(*args, **kwargs) -> stages.Lowered:
    """Lower this function for the given arguments.

    A lowered function is staged out of Python and translated to a
    compiler's input language, possibly in a backend-dependent
    manner. It is ready for compilation but not yet compiled.

    Returns:
      A ``Lowered`` instance representing the lowering.
    """
    closed_fun, in_tree, args_flat, donated_invars = _prepare_jit(
        fun, static_argnums, static_argnames, donate_argnums, args, kwargs)
    flat_fun, out_tree = flatten_fun(closed_fun, in_tree)
    arg_specs_and_devices = map(arg_spec, args_flat)
    if jax.config.jax_dynamic_shapes:
      axes_specs = (None if abstracted_axes is None else
                    _flat_axes_specs(abstracted_axes, *args, **kwargs))
      in_type = pe.infer_lambda_input_type(axes_specs, args_flat)
      flat_fun = lu.annotate(flat_fun, in_type)
      in_avals = [aval for aval, explicit in in_type if explicit]
    else:
      if abstracted_axes:
        raise ValueError("abstracted_axes must be used with --jax_dynamic_shapes")
      in_avals, _ = unzip2(arg_specs_and_devices)
    computation = dispatch.lower_xla_callable(
        flat_fun, device, backend, flat_fun.__name__, donated_invars, True,
        keep_unused, *arg_specs_and_devices)
    return stages.Lowered.from_flat_info(
        computation, in_tree, in_avals, donate_argnums, out_tree())

  return lower
