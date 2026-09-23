def _prepare_pmap(fun, in_axes, out_axes, static_broadcasted_tuple,
                  donate_tuple, global_arg_shapes, devices, args, kwargs):
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
      dyn_global_arg_shapes = global_arg_shapes

    if isinstance(global_arg_shapes, tuple):
      dyn_global_arg_shapes = tuple(global_arg_shapes[i] for i in dyn_argnums)
    else:
      dyn_global_arg_shapes = global_arg_shapes
  else:
    dyn_args, dyn_in_axes = args, in_axes
    dyn_global_arg_shapes = global_arg_shapes
  args, in_tree = tree_flatten((dyn_args, kwargs))

  if donate_tuple:
    donated_invars = donation_vector(donate_tuple, dyn_args, kwargs)
  else:
    donated_invars = (False,) * len(args)
  in_axes_flat = tuple(flatten_axes("pmap in_axes", in_tree, (dyn_in_axes, 0)))
  global_arg_shapes_flat = tuple(flatten_axes(
      "pmap global_arg_shapes", in_tree, (dyn_global_arg_shapes, None),
      kws=True))
  local_axis_size = _mapped_axis_size(
      in_tree, args, in_axes_flat, "pmap", kws=True)

  for arg in args:
    _check_arg(arg)

  flat_fun, out_tree = flatten_fun(f, in_tree)

  if config.jax_array:
    from jax.experimental.array import Array
    if any(not isinstance(a, Array) for a in args):
      raise ValueError('All arguments to pmap when `config.jax_array` is '
                       'enabled should be `Array`s.')
    arr_devices = _check_in_pmap_sharding_with_arrays(args, in_axes_flat, devices)
    if devices is None and arr_devices is not None:
      devices = arr_devices

  if any(out_axis is None for out_axis in tree_flatten(out_axes)):
    raise NotImplementedError("None out_axes in pmap are not supported yet")
  # NOTE: We don't put out_tree() in the closure, because it's (1) non-hashable,
  #       (2) depends deterministically on flat_fun (at least that's the assumption
  #       that we make).
  if out_axes == 0:
    # TODO(apaszke,mattjj): flatten_axes assumes that the output pytree is
    #   functorial (i.e. it can hold leaves of any type), but some user code
    #   breaks this assumption. This is a stop-gap solution to keep the old
    #   out_axes == 0 path working as we look for a better solution.
    out_axes_thunk = HashableFunction(
        lambda: (0,) * out_tree().num_leaves,
        closure=out_axes)
  else:
    # out_axes_thunk closes over the out_axes, they are flattened here to make
    # them hashable.
    out_axes_leaves, out_axes_treedef = tree_flatten(out_axes)
    out_axes_thunk = HashableFunction(
        lambda: tuple(flatten_axes("pmap out_axes", out_tree(),
                                    tree_unflatten(out_axes_treedef,
                                                  list(out_axes_leaves)))),
        closure=(tuple(out_axes_leaves), out_axes_treedef))

  return PmapCallInfo(flat_fun=flat_fun,
                      in_tree=in_tree,
                      out_tree=out_tree,
                      flat_args=args,
                      donated_invars=donated_invars,
                      in_axes_flat=in_axes_flat,
                      local_axis_size=local_axis_size,
                      global_arg_shapes_flat=global_arg_shapes_flat,
                      out_axes_thunk=out_axes_thunk,
                      devices=None if devices is None else tuple(devices))
