def _hlo_unshard(ctx: mlir.LoweringRuleContext, aval, axis_env, out_axis, xs, platform):
  if aval is core.abstract_token:
    return xs
  elif isinstance(aval, core.ShapedArray):
    x, = xs
    # TODO(mattjj): remove this logic when AllReduce PRED supported on CPU / GPU
    convert_bool = (np.issubdtype(aval.dtype, np.bool_)
                    and platform in ('cpu', 'gpu'))
    if convert_bool:
      aval = aval.update(dtype=np.dtype(np.float32))
      x = hlo.ConvertOp(mlir.aval_to_ir_type(aval), x).result

    dims = list(aval.shape)
    padded_aval = aval.update(shape=[axis_env.sizes[-1]] + dims)
    padded = mlir.full_like_aval(ctx, 0, padded_aval)
    zero = mlir.ir_constant(np.zeros((), dtype=np.uint32))
    idxs = [_unravel_index_hlo(axis_env)] + [zero] * len(dims)
    broadcast_result = hlo.BroadcastOp(
        x, mlir.dense_int_elements([1])).result
    padded = hlo.DynamicUpdateSliceOp(padded, broadcast_result, idxs).result
    replica_groups = mlir.dense_int_elements(
      axis_groups(axis_env, axis_env.names[-1]))
    out = hlo.CrossReplicaSumOp(padded, replica_groups).result
    if out_axis != 0:
      # TODO(apaszke,mattjj): Change the indices to DynamicUpdateSlice instead
      perm = list(range(1, len(dims)))
      perm.insert(out_axis, 0)
      transposed_dims = list(dims)
      transposed_dims.insert(out_axis, axis_env.sizes[-1])
      aval = aval.update(shape=transposed_dims)
      out = hlo.TransposeOp(out, mlir.dense_int_elements(perm)).result

    # TODO(mattjj): remove this logic when AllReduce PRED supported on CPU / GPU
    if convert_bool:
      float_zero = mlir.full_like_aval(ctx, 0, padded_aval)
      out = hlo.CompareOp(
          out,
          float_zero,
          hlo.ComparisonDirectionAttr.get("NE"),
          compare_type=hlo.ComparisonTypeAttr.get("FLOAT")).result
    return out
  else:
    raise TypeError(aval)
