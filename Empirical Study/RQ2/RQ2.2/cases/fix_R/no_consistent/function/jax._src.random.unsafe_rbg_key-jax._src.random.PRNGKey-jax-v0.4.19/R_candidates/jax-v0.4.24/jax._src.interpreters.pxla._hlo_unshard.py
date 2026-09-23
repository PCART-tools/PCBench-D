def _hlo_unshard(ctx: mlir.LoweringRuleContext, aval, axis_env, out_axis, xs):
  if aval is core.abstract_token:
    return xs
  elif isinstance(aval, core.ShapedArray):
    x, = xs
    dims = list(aval.shape)
    padded_aval = aval.update(shape=[axis_env.sizes[-1]] + dims)
    padded = mlir.full_like_aval(ctx, 0, padded_aval)
    zero = mlir.ir_constant(np.zeros((), dtype=np.uint32))
    idxs = [_unravel_index_hlo(axis_env)] + [zero] * len(dims)
    broadcast_result = hlo.broadcast(x, mlir.dense_int_array([1]))
    padded = hlo.dynamic_update_slice(padded, broadcast_result, idxs)
    replica_groups = mlir.dense_int_elements(
      axis_groups(axis_env, axis_env.names[-1]))
    out = hlo.cross_replica_sum(padded, replica_groups)
    if out_axis != 0:
      # TODO(apaszke,mattjj): Change the indices to DynamicUpdateSlice instead
      perm = list(range(1, len(dims)))
      perm.insert(out_axis, 0)
      transposed_dims = list(dims)
      transposed_dims.insert(out_axis, axis_env.sizes[-1])
      out = hlo.transpose(out, mlir.dense_int_array(perm))

    return out
  else:
    raise TypeError(aval)
