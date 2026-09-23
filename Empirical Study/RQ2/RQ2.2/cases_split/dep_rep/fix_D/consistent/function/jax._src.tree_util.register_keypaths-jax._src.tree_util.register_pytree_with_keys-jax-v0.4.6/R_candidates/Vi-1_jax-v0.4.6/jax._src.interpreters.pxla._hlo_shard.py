def _hlo_shard(aval, axis_env, xs, in_axis):
  if aval is core.abstract_token:
    return xs
  elif isinstance(aval, core.ShapedArray):
    x, = xs
    dims = list(aval.shape)
    zero = mlir.ir_constant(np.zeros((), dtype=np.uint32))
    idxs = [zero] * len(dims)
    idxs.insert(in_axis, _unravel_index_hlo(axis_env))
    dims_unsqueezed = dims.copy()
    dims_unsqueezed.insert(in_axis, 1)
    dynamic_slice_result = hlo.DynamicSliceOp(
        x, idxs, mlir.dense_int_elements(dims_unsqueezed)).result
    return [
      hlo.ReshapeOp(mlir.aval_to_ir_type(aval), dynamic_slice_result).result
    ]
  else:
    raise TypeError(aval)
