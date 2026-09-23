def map_transpose(primitive, params, call_jaxpr, args, ct, _, reduce_axes):
  all_args, in_tree_def = tree_flatten(((), args, ct))  # empty consts
  fun = lu.hashable_partial(lu.wrap_init(backward_pass), call_jaxpr, reduce_axes, False)
  fun, nz_arg_cts = nonzero_outputs(fun)
  fun, out_tree = flatten_fun_nokwargs(fun, in_tree_def)
  # Preserve axis for primal arguments, skip tangents (represented as undefined primals).
  in_axes, out_axes = params['in_axes'], params['out_axes']
  new_in_axes = (*[axis for axis, x in zip(in_axes, args)
                   if not is_undefined_primal(x)],
                 *[axis for axis, x in zip(out_axes, ct)
                   if type(x) is not Zero])
  # The interim strategy we use below (until avals-with-names) only works
  # when all outputs are mapped.
  assert all(out_axis is not None for out_axis in out_axes), out_axes
  # NOTE: This assumes that the output cotangents being zero is a deterministic
  #       function of which input cotangents were zero.
  @as_hashable_function(closure=(in_axes, tuple(type(c) is Zero for c in ct)))
  def out_axes_thunk():
    return tuple(axis or 0 for axis, nz in zip(in_axes, nz_arg_cts()) if nz)
  new_params = dict(params, name=wrap_name(params['name'], 'transpose'),
                    in_axes=new_in_axes, out_axes_thunk=out_axes_thunk)
  del new_params['out_axes']
  update_params = call_transpose_param_updaters.get(primitive)
  if update_params:
    new_params = update_params(new_params, map(is_undefined_primal, args),
                               [type(x) is not Zero for x in ct])
  out_flat = primitive.bind(fun, *all_args, **new_params)
  arg_cts = tree_unflatten(out_tree(), out_flat)

  # The freevars are being fanned out (not mapped). During transpose the
  # dual of fan-out is fan-in-sum. We apply it to the unmapped invars.
  assert len(in_axes) == len(arg_cts)
  def unmap_zero(zero, in_axis):
    return (zero if in_axis is None else
            Zero(core.unmapped_aval(params['axis_size'], params['axis_name'], in_axis, zero.aval)))
  arg_cts = (unmap_zero(arg_ct, in_axis) if type(arg_ct) is Zero else
             arg_ct if in_axis is not None else
             arg_ct.sum(0)
             for arg_ct, in_axis in zip(arg_cts, in_axes))
  return tuple(arg_cts)
