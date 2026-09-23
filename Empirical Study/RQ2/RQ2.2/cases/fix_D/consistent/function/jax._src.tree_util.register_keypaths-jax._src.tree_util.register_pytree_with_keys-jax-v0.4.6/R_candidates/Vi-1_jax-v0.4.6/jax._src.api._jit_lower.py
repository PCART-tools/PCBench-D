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
    if jax.config.jax_array:
      if hasattr(x, 'sharding'):
        if isinstance(x.sharding, PmapSharding):
          return aval, None
        # If `x` has a sharding attribute but not `_committed` attribute,
        # assume that `x` is committed. This might happen when the input is
        # a `ShapedDtypeStruct` or `types.SimpleNamespace`, etc that might
        # only have a `sharding` attribute on them.
        return aval, (pjit.to_gspmd_sharding(x.sharding, x.ndim)
                      if getattr(x, '_committed', True) else None)
      else:
        return aval, None
    else:
      device = getattr(x, '_device', None)
      return aval, device

  @api_boundary
  def lower(*args, _experimental_lowering_platform: Optional[str] = None,
            **kwargs) -> stages.Lowered:
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
    in_avals: Sequence[core.AbstractValue]
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
      if any(not core.is_constant_shape(a.shape) for a in in_avals):
        # TODO(b/262808613): Do not drop unused inputs when we have
        # shape polymorphism, to ensure that we can always derive
        # the dimension variables from the kept inputs.
        nonlocal keep_unused
        keep_unused = True
    if jax.config.jax_array:
      computation = dispatch.sharded_lowering(
          flat_fun, device, backend, flat_fun.__name__, donated_invars, True,
          keep_unused, lowering_platform=_experimental_lowering_platform,
          *arg_specs_and_devices)
      return stages.Lowered.from_flat_info(
          computation, in_tree, in_avals, donate_argnums, out_tree())
    else:
      computation = dispatch.lower_xla_callable(
          flat_fun, device, backend, flat_fun.__name__, donated_invars, True,
          keep_unused, lowering_platform=_experimental_lowering_platform,
          *arg_specs_and_devices)
      return stages.Lowered.from_flat_info(
          computation, in_tree, in_avals, donate_argnums, out_tree())

  return lower
