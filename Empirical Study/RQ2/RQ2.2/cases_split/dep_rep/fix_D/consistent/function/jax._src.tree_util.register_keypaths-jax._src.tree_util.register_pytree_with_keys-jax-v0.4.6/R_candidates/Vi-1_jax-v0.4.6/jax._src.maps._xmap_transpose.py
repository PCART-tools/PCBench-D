def _xmap_transpose(params, call_jaxpr, args, cts_in, cts_in_avals, reduce_axes):
  all_args, in_tree_def = tree_flatten(((), args, cts_in))  # empty consts
  fun = lu.hashable_partial(
      lu.wrap_init(ad.backward_pass),
      call_jaxpr, reduce_axes + tuple(params['global_axis_sizes'].keys()), False)
  fun, nz_arg_cts = ad.nonzero_outputs(fun)
  fun, out_tree = flatten_fun_nokwargs(fun, in_tree_def)
  # Preserve axis for primal arguments, skip tangents (represented as undefined primals).
  in_axes, out_axes = params['in_axes'], params['out_axes']
  new_in_axes = (*(axis for axis, x in zip(in_axes, args) if not ad.is_undefined_primal(x)),
                 *(axis for axis, x in zip(out_axes, cts_in) if type(x) is not ad.Zero))
  # NOTE: This assumes that the output cotangents being zero is a deterministic
  #       function of which input cotangents were zero.
  @as_hashable_function(closure=(in_axes, tuple(type(c) is ad.Zero for c in cts_in)))
  def out_axes_thunk():
    return tuple(axis for axis, nz in zip(in_axes, nz_arg_cts()) if nz)
  new_params = dict(params,
                    name=wrap_name(params['name'], 'transpose'),
                    in_axes=new_in_axes,
                    out_axes_thunk=out_axes_thunk,
                    donated_invars=(False,) * len(new_in_axes),
                    spmd_out_axes_thunk=None)
  del new_params['out_axes']
  del new_params['spmd_out_axes']
  out_flat = xmap_p.bind(fun, *all_args, **new_params)
  arg_cts = tree_unflatten(out_tree(), out_flat)

  axis_resource_count = _get_axis_resource_count(
      params['axis_resources'], params['resource_env'],
      params['in_positional_semantics'])
  local_axis_sizes = {
      axis: axis_resource_count[axis].to_local(params['out_positional_semantics'], global_size)
      for axis, global_size in params['global_axis_sizes'].items()
  }
  def unmap_zero(zero, axes):
    return ad.Zero(_insert_aval_axes(zero.aval, axes, local_axis_sizes))
  return tuple(unmap_zero(arg_ct, in_axis) if type(arg_ct) is ad.Zero else arg_ct
               for arg_ct, in_axis in zip(arg_cts, in_axes))
