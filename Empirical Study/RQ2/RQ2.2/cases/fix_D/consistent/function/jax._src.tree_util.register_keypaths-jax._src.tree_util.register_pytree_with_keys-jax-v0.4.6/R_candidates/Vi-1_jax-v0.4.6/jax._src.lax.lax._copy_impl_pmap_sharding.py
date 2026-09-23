def _copy_impl_pmap_sharding(sharded_dim, *args, **kwargs):
  axis_name, static_broadcasted_tuple, donate_tuple = api._shared_code_pmap(
    _identity_fn, None, (), (), sharded_dim, sharded_dim)
  p = api._prepare_pmap(
      _identity_fn, sharded_dim, sharded_dim, static_broadcasted_tuple,
      donate_tuple, None, None, None, None, args, kwargs)
  out_flat =  pxla.xla_pmap_impl(
      p.flat_fun, *p.flat_args, backend=None, axis_name=axis_name,
      axis_size=p.local_axis_size, global_axis_size=p.global_axis_size,
      devices=p.devices, in_axes=p.in_axes_flat,
      out_axes_thunk=p.out_axes_thunk, name=p.flat_fun.__name__,
      donated_invars=p.donated_invars,
      global_arg_shapes=p.global_arg_shapes_flat,
      is_explicit_global_axis_size=p.is_explicit_global_axis_size,
  )
  return tree_util.tree_unflatten(p.out_tree(), out_flat)
