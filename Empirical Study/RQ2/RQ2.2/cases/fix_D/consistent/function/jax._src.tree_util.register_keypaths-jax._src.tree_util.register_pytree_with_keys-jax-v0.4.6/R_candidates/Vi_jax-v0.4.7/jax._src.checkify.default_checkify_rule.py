def default_checkify_rule(primitive: core.Primitive, error: Error,
                          enabled_errors, *invals: core.Value,
                          **params: Any) -> Tuple[Error, Sequence[core.Value]]:
  """Default rule for primitives in `checkify` interpreter."""
  if 'call_jaxpr' not in params:
    # Default non-HOP case: just call primitive and don't update error.
    return error, primitive.bind(*invals, **params)

  # Code below handles call- and map-primitives, by recursively calling
  # checkify_jaxpr.
  err_vals, err_tree = jtu.tree_flatten(error)
  num_error_vals = len(err_vals)
  if 'donated_invars' in params:
    params = dict(params, donated_invars=(*[False]*num_error_vals,
                                          *params['donated_invars']))

  # call_jaxpr handling
  call_jaxpr = params.pop('call_jaxpr')
  partial_checkify = lu.hashable_partial(lu.wrap_init(
      checkify_jaxpr_flat), call_jaxpr, (), enabled_errors, err_tree)
  partial_checkify, metadata = _flatten_and_get_error_metadata_thunk(
      partial_checkify)

  # map-specific params handling.
  if isinstance(primitive, core.MapPrimitive):
    # Update `in_axes` and `out_axes_thunk` params for map primitive.
    out_val_axes = params.pop('out_axes')

    @as_hashable_function(closure=out_val_axes)
    def out_axes_thunk():
      out_err_num = metadata()[0].num_leaves - len(out_val_axes)
      return (*(0,)*out_err_num, *out_val_axes)

    params = dict(params,
                  in_axes=(*(None,)*num_error_vals, *params['in_axes']),
                  out_axes_thunk=out_axes_thunk)

  all_vals = primitive.bind(partial_checkify, *err_vals, *invals, **params)

  out_tree, _ = metadata()
  error, out_vals = tree_unflatten(out_tree, all_vals)
  if isinstance(primitive, core.MapPrimitive):
    error = _reduce_any_error(error)
  return error, out_vals
