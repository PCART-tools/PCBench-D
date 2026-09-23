def _masked_swap_lowering_rule(
    ctx: LoweringRuleContext, ref, val, *args, args_tree, masked, **params
):
  del params
  if masked:
    raise NotImplementedError
  ref_block_shape, *_ = ctx.block_shapes
  ref_aval, val_aval, *_ = ctx.avals_in
  (aval_out,) = ctx.avals_out
  if not isinstance(val, ir.Value):
    val = ir_constant(val, mlir_type=mlir.dtype_to_ir_type(val_aval.dtype))
  idx, *_ = tree_util.tree_unflatten(args_tree, args)
  idx_aval, *_ = tree_util.tree_unflatten(args_tree, ctx.avals_in[2:])
  indices = idx.indices
  if any(
      not isinstance(a, primitives.Slice) and a.shape != ()
      for a in idx_aval.indices
  ):
    raise ValueError("Cannot do int indexing on TPU")
  if not ref_block_shape:
    raise NotImplementedError(
        "Indexing into a ()-shaped Ref not yet supported on TPU.")
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
  mem_slice_shape = list(aval_out.shape)
  for i, a in enumerate(idx_aval.indices):
    if not isinstance(a, primitives.Slice):
      mem_slice_shape.insert(i, 1)
  mem_slice_shape_iter = iter(mem_slice_shape)
  mem_slice_shape = [
      1 if b is core.mapped else next(mem_slice_shape_iter)
      for b in ref_block_shape
  ]
  mem_aval = aval_out.update(shape=tuple(mem_slice_shape))
  mem_aval_vec_type = ir.VectorType.get(mem_aval.shape,
                                        mlir.dtype_to_ir_type(mem_aval.dtype))
  result = vector.LoadOp(mem_aval_vec_type, ref, mlir_indices).result
  if mem_aval != aval_out:
    # We are slicing a scalar so provided dummy 1 indices
    result_vec_type = ir.VectorType.get(aval_out.shape,
                                        mlir.dtype_to_ir_type(aval_out.dtype))
    result = vector.ShapeCastOp(result_vec_type, result).result
    val_vec_type = ir.VectorType.get(mem_aval.shape,
                                     mlir.dtype_to_ir_type(mem_aval.dtype))
    val = vector.ShapeCastOp(val_vec_type, val).result
  vector.StoreOp(val, ref, mlir_indices)
  return result
