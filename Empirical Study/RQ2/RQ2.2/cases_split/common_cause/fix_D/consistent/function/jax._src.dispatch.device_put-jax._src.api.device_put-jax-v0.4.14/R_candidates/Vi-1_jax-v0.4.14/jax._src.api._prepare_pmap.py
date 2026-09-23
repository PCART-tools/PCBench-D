def _prepare_pmap(fun, in_axes, out_axes, static_broadcasted_tuple,
                  donate_tuple, in_devices, backend_name,
                  axis_size, args, kwargs):
  if in_devices is not None and len(in_devices) == 0:
    raise ValueError("'devices' argument to pmap must be non-empty, or None.")

  dbg = debug_info('pmap', fun, args, kwargs, static_broadcasted_tuple, ())

  f = lu.wrap_init(fun)
  if static_broadcasted_tuple:
    if max(static_broadcasted_tuple) >= len(args):
      raise ValueError(
          f"pmapped function has static_broadcasted_argnums={static_broadcasted_tuple}"
          f" but was called with only {len(args)} positional "
          f"argument{'s' if len(args) > 1 else ''}. "
          "All static broadcasted arguments must be passed positionally.")
    dyn_argnums = [i for i in range(len(args))
                   if i not in static_broadcasted_tuple]
    f, dyn_args = argnums_partial(f, dyn_argnums, args)

    if isinstance(in_axes, tuple):
      dyn_in_axes = tuple(in_axes[i] for i in dyn_argnums)
    else:
      dyn_in_axes = in_axes
  else:
    dyn_args, dyn_in_axes = args, in_axes
  args, in_tree = tree_flatten((dyn_args, kwargs))

  if donate_tuple and not config.jax_debug_nans:
    donated_invars = donation_vector(donate_tuple, (), dyn_args, kwargs)
  else:
    donated_invars = (False,) * len(args)
  try:
    in_axes_flat = tuple(broadcast_prefix((dyn_in_axes, 0), (dyn_args, kwargs),
                                          is_leaf=lambda x: x is None))
  except ValueError:
    e, *_ = prefix_errors((dyn_in_axes, 0), (dyn_args, kwargs))
    ex = e('pmap in_axes')
    msg, = ex.args
    msg += ("\n\nThe 'full pytree' here is the tuple of arguments passed "
            "positionally to the pmapped function, and the value of `in_axes` "
            "must be a tree prefix of that tuple. But it was not a prefix.")
    if kwargs:
      msg += ("\n\nWhen some arguments are passed by keyword to the pmapped "
              "function, they are not included in the comparison to `in_axes`. "
              "Instead, each argument passed by keyword is mapped over its "
              "leading axis. See the description of `in_axes` in the `pmap` "
              "docstring: "
              "https://jax.readthedocs.io/en/latest/_autosummary/jax.pmap.html#jax.pmap")
    msg += ("\n\nCheck that the value of the `in_axes` argument to `pmap` "
            "is a tree prefix of the tuple of arguments passed positionally to "
            "the pmapped function.")
    raise ValueError(msg) from None
  local_axis_size = _mapped_axis_size(fun, in_tree, args, in_axes_flat, "pmap")

  f, res_paths = result_paths(f)
  f, out_axes_thunk = flat_out_axes(f, out_axes)
  flat_fun, out_tree = flatten_fun(f, in_tree)
  flat_fun = debug_info_final(flat_fun, dbg, res_paths)

  is_explicit_global_axis_size = axis_size is not None
  global_axis_size = _get_global_axis_size(local_axis_size, in_devices,
                                           backend_name, axis_size)
  return PmapCallInfo(flat_fun=flat_fun,
                      in_tree=in_tree,
                      out_tree=out_tree,
                      flat_args=args,
                      donated_invars=donated_invars,
                      in_axes_flat=in_axes_flat,
                      local_axis_size=local_axis_size,
                      out_axes_thunk=out_axes_thunk,
                      devices=None if in_devices is None else tuple(in_devices),
                      global_axis_size=global_axis_size,
                      is_explicit_global_axis_size=is_explicit_global_axis_size)
