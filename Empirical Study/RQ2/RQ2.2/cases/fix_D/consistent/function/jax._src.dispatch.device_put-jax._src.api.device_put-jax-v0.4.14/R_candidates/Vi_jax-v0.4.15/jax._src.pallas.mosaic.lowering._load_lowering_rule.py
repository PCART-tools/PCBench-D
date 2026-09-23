def _load_lowering_rule(
    ctx: LoweringRuleContext, ref, *args, args_tree, masked, **params
):
  ref_type = ir.MemRefType(ref.type)
  is_smem_load = str(ref_type.memory_space) == "#tpu.memory_space<smem>"
  del params
  if masked:
    raise NotImplementedError
  ref_aval, *_ = ctx.avals_in
  (aval_out,) = ctx.avals_out
  ref_block_shape, *_ = ctx.block_shapes
  idx, *_ = tree_util.tree_unflatten(args_tree, args)
  idx_aval, *_ = tree_util.tree_unflatten(args_tree, ctx.avals_in[1:])
  indices = idx.indices
  if not ref_block_shape:
    raise NotImplementedError(
        "Indexing into a ()-shaped Ref not yet supported on TPU.")
  if any(
      not isinstance(a, primitives.Slice) and a.shape != ()
      for a in idx_aval.indices
  ):
    raise ValueError("Cannot do int indexing on TPU")
  starts = tuple(
      i.start if isinstance(i, primitives.Slice) else i for i in indices
  )
  mlir_indices = [
      s if isinstance(s, primitives.Slice) else _make_index(s) for s in starts
  ]
  # Need to now insert indexing the 0-th element for mapped dimensions
  idx_iter = iter(mlir_indices)
  mlir_indices = [
      _make_index(0) if b is core.mapped else next(idx_iter)
      for b in ref_block_shape
  ]
  assert len(mlir_indices) == len(ref_block_shape)
  load_shape = list(aval_out.shape)
  for i, a in enumerate(idx_aval.indices):
    if not isinstance(a, primitives.Slice):
      load_shape.insert(i, 1)
  assert len(load_shape) == len(ref_aval.shape)
  load_shape_iter = iter(load_shape)
  load_shape = [
      1 if b is core.mapped else next(load_shape_iter) for b in ref_block_shape
  ]
  load_aval = aval_out.update(shape=tuple(load_shape))
  if is_smem_load:
    if ctx.avals_out[0].shape:
      raise ValueError("Can only load scalars from SMEM:")
    return memref.LoadOp(ref, mlir_indices).result
  else:
    load_val = vector.LoadOp(aval_to_ir_type(load_aval), ref, mlir_indices).result
  if load_aval == aval_out:
    return load_val
  vec_type = ir.VectorType.get(aval_out.shape,
                               mlir.dtype_to_ir_type(aval_out.dtype))
  return vector.ShapeCastOp(vec_type, load_val).result
