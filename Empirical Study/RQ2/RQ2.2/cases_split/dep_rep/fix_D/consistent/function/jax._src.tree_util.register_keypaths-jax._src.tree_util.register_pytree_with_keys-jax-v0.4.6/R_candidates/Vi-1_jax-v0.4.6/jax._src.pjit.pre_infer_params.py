def pre_infer_params(fun, in_shardings, out_shardings,
                     donate_argnums, static_argnums, static_argnames, device,
                     backend, abstracted_axes):
  # TODO(yashkatariya, mattjj): Remove when pjit supports dynamic shapes.
  if jax.config.jax_dynamic_shapes:
    raise ValueError("Dynamic shapes is not supported with pjit yet.")
  if abstracted_axes and not jax.config.jax_dynamic_shapes:
    raise ValueError("abstracted_axes must be used with --jax_dynamic_shapes")

  check_callable(fun)

  if (not jax.config.jax_array and
      (_is_unspecified(in_shardings) or _is_unspecified(out_shardings))):
    raise ValueError(
        "in_shardings and out_shardings should not "
        "be the unspecified singleton value. Please enable `jax.Array` to use "
        "this feature. You can use jax.config.update('jax_array', True) or "
        "set the environment variable  JAX_ARRAY=1 , or set the `jax_array` "
        "boolean flag to something true-like.")

  if backend is not None or device is not None:
    warnings.warn(
        'backend and device argument on jit is deprecated. You can use a '
        '`jax.sharding.Mesh` context manager or device_put the arguments '
        'before passing them to `jit`. Please see '
        'https://jax.readthedocs.io/en/latest/notebooks/Distributed_arrays_and_automatic_parallelization.html '
        'for more information.', DeprecationWarning)
    if device is not None and backend is not None:
      raise ValueError("can't specify both a device and a backend for jit, "
                       f"got {device=} and {backend=}")
    if not _is_unspecified(in_shardings):
      raise ValueError('If backend or device is specified on jit, then '
                       'in_shardings should not be specified.')
    if not _is_unspecified(out_shardings):
      raise ValueError('If backend or device is specified on jit, then '
                       'out_shardings should not be specified.')

  if isinstance(in_shardings, list):
    # To be a tree prefix of the positional args tuple, in_axes can never be a
    # list: if in_axes is not a leaf, it must be a tuple of trees. However,
    # in cases like these users expect tuples and lists to be treated
    # essentially interchangeably, so we canonicalize lists to tuples here
    # rather than raising an error. https://github.com/google/jax/issues/2367
    in_shardings = tuple(in_shardings)

  in_shardings, _, _ = _prepare_axis_resources(in_shardings, 'in_shardings')
  out_shardings, _, _ = _prepare_axis_resources(out_shardings, 'out_shardings')

  donate_argnums, static_argnums, static_argnames = resolve_argnums(
      fun, donate_argnums, static_argnums, static_argnames)

  return (in_shardings, out_shardings, donate_argnums, static_argnums,
          static_argnames)
